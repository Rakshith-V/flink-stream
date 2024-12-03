FROM flink:1.20.0-scala_2.12


COPY requirements.txt ./requirements.txt
# Install Python
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python
# Download the Kafka connector JAR
RUN wget -q -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.3.0-1.20/flink-sql-connector-kafka-3.3.0-1.20.jar

RUN pip install -r requirements.txt

# Set up environment
ENV PYTHONPATH=$PYTHONPATH:/opt/flink

COPY aggregation_flink.py /opt/flink/jobs/aggregation_flink.py
COPY application-ad.yml /opt/flink/jobs/application-ad.yml


# Set up default command (if not already in your Dockerfile)
CMD ["flink", "jobmanager"]
