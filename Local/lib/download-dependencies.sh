#!/bin/bash

# Download flink-connector-jdbc jar
curl -o flink-connector-jdbc-3.1.2-1.18.jar https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.2-1.18/flink-connector-jdbc-3.1.2-1.18.jar

# Download flink-sql-connector-kafka jar
curl -o flink-sql-connector-kafka-3.1.0-1.18.jar https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.1.0-1.18/flink-sql-connector-kafka-3.1.0-1.18.jar

# Download postgresql jar
curl -o postgresql-42.7.3.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar
