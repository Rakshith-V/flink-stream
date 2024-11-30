#!/bin/bash
KAFKA_BROKER=$1
TOPIC_NAME=$2
PARTITIONS=${3:-1}
REPLICATION=${4:-1}

kafka-topics --create --topic "$TOPIC_NAME" \
             --bootstrap-server "$KAFKA_BROKER" \
             --partitions "$PARTITIONS" \
             --replication-factor "$REPLICATION"
