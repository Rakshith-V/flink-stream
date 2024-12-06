import json
from aiokafka import AIOKafkaProducer
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.formats.json import JsonRowSerializationSchema
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.common.time import Time as FlinkTime
from pyflink.common.time import Duration
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common.typeinfo import Types
import requests
import yaml
import asyncio
import warnings
warnings.filterwarnings("ignore")

CONFIG_FILE_PATH = "application.yml"


async def send_to_kafka(producer, row):
    """Send the aggregated list of JSONs of 30-second window to Kafka"""
    message = json.dumps(row).encode("utf-8")
    metadata = await producer.send_and_wait(produce_topic, message)
    print(f"Flink-aggregated data sent to topic {metadata.topic} at offset {metadata.offset}: {message}")


def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    

def parse_and_filter_json(data):
    """Parses JSON and removes the 'user_session' field."""
    record = json.loads(data)
    del record["user_session"]
    return json.dumps(record)


def send_to_api(batch):
    """Sends a batch of JSON records to an API endpoint."""
    try:
        response = requests.post(api_endpoint, json=batch)
        if response.status_code == 200:
            print(f"Successfully sent batch: {response.json()}")
        else:
            print(f"Failed to send batch: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending data to API: {e}")


async def main():

    producer = AIOKafkaProducer(bootstrap_servers=brokers)
    await producer.start()
    # Set up the environment
    env = StreamExecutionEnvironment.get_execution_environment()

    # Define Kafka source
    kafka_source = FlinkKafkaConsumer(
        topics=consume_topic,
        deserialization_schema=SimpleStringSchema(),
        properties={
            'bootstrap.servers': brokers,
            'group.id': 'flink-group'
        }
    )
    kafka_stream = env.add_source(kafka_source)

    kafka_stream = kafka_stream.assign_timestamps_and_watermarks(
        WatermarkStrategy
        .for_bounded_out_of_orderness(Duration.of_seconds(5))
    )

    # Process the JSON data
    processed_stream = kafka_stream.map(parse_and_filter_json)

    # Windowed aggregation for value = aggregation_window from config file
    windowed_stream = (
        processed_stream.key_by(lambda x: 1)
        .window_all(TumblingProcessingTimeWindows.of(FlinkTime.seconds(aggregation_window)))
        .reduce(lambda acc, value: acc + [value] if isinstance(acc, list) else [value])
    )

    # windowed_stream.print()
    # windowed_stream.map(print_result)
    # print(f"Windowed Stream: {windowed_stream}")

    # Send to API
    # windowed_stream.add_sink(lambda batch: send_to_api(batch))
    # try:
    #     windowed_stream.map(lambda batch: print(f"Received batch, triggering API...") or send_to_api(batch))
    # except Exception as ex:
    #     print(f"Exception encountered: {ex}")

    serialization_schema = JsonRowSerializationSchema.builder().with_type_info(
    type_info=Types.ROW([Types.LIST(Types.MAP(Types.STRING(), Types.STRING()))])).build()

    kafka_sink = FlinkKafkaProducer(
        topic="processed_customer_topic",
        serialization_schema=SimpleStringSchema(),
        producer_config={
            'bootstrap.servers': brokers,
            'group.id': 'flink-group'
        }
    )

    with windowed_stream.execute_and_collect() as results:
        for result in results:
            await send_to_kafka(producer, result)

    # windowed_stream.map(lambda batch: json.dumps(batch)).map(lambda x: print(f"Data before sink: {x}")).add_sink(kafka_sink)
    
    # Execute the Flink job
    env.execute("Kafka to API Streaming Job")


if __name__ == "__main__":
    config = load_config(CONFIG_FILE_PATH)

    brokers = config["flink"]["kafka_broker"]
    consume_topic = config["flink"]["consume_topic"]
    produce_topic = config["flink"]["produce_topic"]
    aggregation_window = config["flink"]["aggregation_window"]
    api_endpoint = config["llm_endpoint"]["url"]

    asyncio.run(main())
