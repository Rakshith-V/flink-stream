import json
import csv
import asyncio
from aiokafka import AIOKafkaProducer
import yaml
import time

CONFIG_FILE_PATH = "application.yml"


def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

async def send_to_kafka(producer, row):
    
    message = json.dumps(row).encode("utf-8")
    metadata = await producer.send_and_wait(topic, message)
    print(f"Customer data sent to topic {metadata.topic} at offset {metadata.offset}: {message}")
    

async def main():

    producer = AIOKafkaProducer(bootstrap_servers=brokers)
    await producer.start()

    try:
        for file in csv_files:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                print("File loaded")
                # tasks = [send_to_kafka(producer, row) for row in reader]
                # print("Tasks loaded, ready to gather")
                # await asyncio.gather(*tasks)

                for idx, row in enumerate(reader):
                    # print(f"Sending data at row {idx} to Kafka: {row}")
                    await send_to_kafka(producer, row)
                    time.sleep(delay)

    except Exception as ex:
        print(f"Exception encountered: {ex}")
    finally:
        await producer.stop()


if __name__ == "__main__":
    config = load_config(CONFIG_FILE_PATH)

    brokers = config["kafka"]["broker"]
    topic = config["kafka"]["topic"]
    csv_files = config["csv_files"]
    delay = config["streaming"]["delay"]

    asyncio.run(main())