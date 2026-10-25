from kafka import KafkaProducer, KafkaConsumer
import json

def create_kafka_producer(bootstrap_server: str):
    """Создает продюсера для отправки сообщений в Kafka"""
    return KafkaProducer(
        bootstrap_servers=bootstrap_server,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_kafka_consumer(bootstrap_server: str, group_id: str = "notifications-group"):
    """Создает консьюмера для чтения сообщений из Kafka"""
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_server,
        group_id=group_id,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    consumer.subscribe(['orders_topic'])
    return consumer
