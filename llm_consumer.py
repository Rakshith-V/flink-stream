from aiokafka import AIOKafkaConsumer
import json
import requests
import yaml
import asyncio



# Configuration
CONFIG_FILE_PATH = "application.yml"

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

config = load_config(CONFIG_FILE_PATH)

TOPIC_NAME = config["llm"]["topic"]
BOOTSTRAP_SERVERS = config["kafka"]["broker"]
API_ENDPOINT = config["llm"]["url"]

async def main():
    # Initialize Kafka Consumer
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',  
        enable_auto_commit=True,
        group_id='my_consumer_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    await consumer.start()

    print(f"Listening to Kafka topic: {TOPIC_NAME}")

    async for message in consumer:
        message_value = message.value
        print(f"Consumed message: {message_value}")

        headers = {"Content-Type" : "application/json"}

        try:
            response = requests.post(API_ENDPOINT, json=message_value, headers=headers, verify=False)
            response.raise_for_status()  

            api_response = response.json()
            print(f"API Response: {api_response}")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")


if __name__ == "__main__":
    asyncio.run(main())