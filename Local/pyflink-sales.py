import configparser
import logging
import sys
import os
from json import loads
from datetime import datetime

from pyflink.datastream import StreamExecutionEnvironment,  RuntimeExecutionMode
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common import SimpleStringSchema, WatermarkStrategy, Types
from pyflink.common.typeinfo import RowTypeInfo
from pyflink.common.types import Row
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcConnectionOptions, JdbcExecutionOptions

def convert_timestamp_to_date(timestamp_ms: int):
    timestamp_s = timestamp_ms / 1000.0
    ts = datetime.fromtimestamp(timestamp_s)
    return ts.strftime('%Y-%m-%d %H:%M:%S')

def byte_to_dict(msg):
    if isinstance(msg, str):
        start_index = msg.find('{')
        result = msg[start_index:]
        return loads(result)
    if isinstance(msg, dict):
        return msg
    
def flatten_dict(message, new_key=''):
    data = byte_to_dict(message)
    items = []
    for key, value in data.items():
        new_key = key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)

def update_dtype(msg):
    result = flatten_dict(msg)
    result["orderid"] = str(result["orderid"])
    result["orderunits"] = str(result["orderunits"])
    result["zipcode"] = str(result["zipcode"])
    return result

# convert dict to row
def dict_to_row(msg):
    data = update_dtype(msg)
    data['ordertime'] = convert_timestamp_to_date(data["ordertime"])
    return Row(**data)

def setup_config():
    config_path = 'secrets/app.cfg'

    try:
        config = configparser.ConfigParser()
        config.read(config_path)
    except Exception as e:
        logging.error(f'Configuration file not found: {config_path}')
    return config

def get_dependency_paths(subdirectory='lib'):
    
    current_directory = os.getcwd()
    full_path_to_subdirectory = os.path.join(current_directory, subdirectory)
    
    dependencies = {}
    
    for root, dirs, files in os.walk(full_path_to_subdirectory):
        for file in files:
            if file.endswith('.jar'):
                full_path = os.path.join(root, file)
                url_path = 'file:///' + full_path.replace('\\', '/')
                if 'postgres' in file:
                    dependencies['psql'] = url_path
                elif 'jdbc' in file:
                    dependencies['jdbc'] = url_path
                elif 'kafka' in file:
                    dependencies['kafka'] = url_path
                    
    return dependencies

def main():
    # setup environment    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
    env.set_parallelism(1)

    # add dependencies
    dependencies_paths = get_dependency_paths()
    env.add_jars(dependencies_paths['kafka'],
                 dependencies_paths['jdbc'],
                 dependencies_paths['psql']
                 )
    
    # setup config
    config = setup_config()    
        
    # setup kafka source          
    kafka_source = KafkaSource.builder()\
                        .set_topics(config['kafka']['topic'])\
                        .set_bootstrap_servers(config['kafka']['bootstrap_server'])\
                        .set_group_id('demo_19')\
                        .set_starting_offsets(KafkaOffsetsInitializer.earliest())\
                        .set_property("security.protocol", "SASL_SSL")\
                        .set_property("sasl.mechanism", "PLAIN")\
                        .set_property("sasl.jaas.config", f"org.apache.flink.kafka.shaded.org.apache.kafka.common.security.plain.PlainLoginModule required username=\"{config['security']['username']}\" password=\"{config['security']['password']}\";")\
                        .set_value_only_deserializer(SimpleStringSchema())\
                        .build()

    # define row type
    sales_schema = RowTypeInfo(
        field_names=[
            "ordertime", "orderid", "itemid", "orderunits", "city", "state", "zipcode"
        ],
        field_types=[
            Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING(), Types.STRING()
        ]
    )
    
    # create data stream     
    data_stream = env.from_source(kafka_source, WatermarkStrategy.no_watermarks(), "Kafka Sales")\
                    .map(dict_to_row, sales_schema)
    
    # define jdbc sink options
    jdbc_options = JdbcConnectionOptions.JdbcConnectionOptionsBuilder()\
                    .with_url(config['postgres']['url'])\
                    .with_driver_name('org.postgresql.Driver')\
                    .with_user_name(config['postgres']['username'])\
                    .with_password(config['postgres']['password'])\
                    .build()
    
    # define jdbc sink exceptions            
    jdbc_exceptions = JdbcExecutionOptions.builder()\
                        .with_batch_interval_ms(1000)\
                        .with_batch_size(200)\
                        .with_max_retries(5)\
                        .build()
    
    # define sink sql statement
                
    sink_sql_stmt = f"""
        INSERT INTO public.sales ("ordertime", "orderid", "itemid", "orderunits", "city", "state", "zipcode")
            VALUES (?, ?, ?, ?, ?, ?, ?)
    """  

    # add sink
    data_stream.add_sink(
        JdbcSink.sink(sink_sql_stmt,
                    sales_schema,
                    jdbc_options, 
                    jdbc_exceptions)
        )\
        .name("Sink Sales")

    # execute
    env.execute()
    
if __name__ == '__main__':
    
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    
    main()