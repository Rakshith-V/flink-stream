# FlinkStream
Repository to host code for Final Project for COMPSCI 532.

Pre-requisites:
1. Docker Desktop
2. Conda environment for this project
3. Pip install requirements.txt from in the activated conda environment
4. Meta's LLAMA LLM API Key (request here: )

### Steps to run:

1. In the current project directory, create a conda environment with python3.10 and run  `pip install -r requirements.txt` after activating the conda environment.
2. For torch specifically to work with CUDA and all, run PyTorch installation command for your relevant system from [here]().
1. Run `docker compose up -d` to run Kafka and Flink in detached mode.
2. Run `python customer_producer.py` to produce data in Kafka topic.
3. Modify application.yml for final new additions. Make your own application-*.yml for local testing, they will be igonored by .gitignore.