from kafka import KafkaConsumer
import json
import requests

# Configuration
BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC_NAME = 'ask_llm'
API_ENDPOINT = 'http://127.0.0.1:5000' 

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',  
    enable_auto_commit=True,
    group_id='my_consumer_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f"Listening to Kafka topic: {TOPIC_NAME}")

for message in consumer:
    message_value = message.value
    print(f"Consumed message: {message_value}")

    try:
        response = requests.post(API_ENDPOINT, json=message_value)
        response.raise_for_status()  

        api_response = response.json()
        print(f"API Response: {api_response}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
