# Run PyFlink Locally 

## Dependencies Downloader

### Overview

The lib contains a script to download necessary dependencies for Apache Flink. These dependencies include connectors for JDBC, Kafka, and PostgreSQL, which are essential for integrating Flink with various data sources and sinks.

#### Dependencies

1. **Flink JDBC Connector**:
   - **File**: `flink-connector-jdbc-3.1.2-1.18.jar`
   - **Purpose**: This connector allows Apache Flink to interact with any JDBC-compliant database. It is used to read from and write to databases within Flink applications.

2. **Flink SQL Connector for Kafka**:
   - **File**: `flink-sql-connector-kafka-3.1.0-1.18.jar`
   - **Purpose**: This connector enables Flink to interact with Apache Kafka. It allows Flink to consume data from Kafka topics and produce data to Kafka topics, which is crucial for real-time data processing and stream processing applications.

3. **PostgreSQL JDBC Driver**:
   - **File**: `postgresql-42.7.3.jar`
   - **Purpose**: This driver is necessary for Flink applications that need to connect to a PostgreSQL database. It provides the means to connect, read, and write data from/to PostgreSQL databases.

#### Prerequisites

Ensure that you have `curl` installed on your system.

#### Instruction