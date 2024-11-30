# FlinkStream
Repository to host code for Final Project for COMPSCI 532.

Pre-requisites:
1. Docker Desktop
2. Conda environment for this project
3. Pip install requirements.txt from in the activated conda environment

### Steps to run:

1. Run `docker compose up -d` to run Kafka and Flink in detached mode.
2. Run `python customer_producer.py` to produce data in Kafka topic.
3. Modify application.yml for final new additions. Make your own application-*.yml for local testing, they will be igonored by .gitignore.