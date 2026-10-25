import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, create_tables
from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.kafka import KafkaContainer
# --- Контейнеры ---

@pytest.fixture(scope="module")
def postgres_container():
    """Поднимает контейнер с PostgreSQL"""
    # Используем легковесный образ Alpine
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="module")
def kafka_container():
    """Поднимает контейнер с Apache Kafka"""
    with KafkaContainer() as kafka:
        yield kafka

# --- Сессия базы данных ---

@pytest.fixture(scope="module")
def db_session(postgres_container):
    """Создает таблицы и возвращает сессию БД"""
    # Получаем динамический URL подключения из контейнера
    db_url = postgres_container.get_connection_url()
    
    engine = create_engine(db_url)
    create_tables(engine) # Создаем таблицу orders
    
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = TestingSessionLocal()
    
    yield session
    
    session.close()

# --- Kafka клиенты ---

@pytest.fixture(scope="module")
def kafka_producer(kafka_container):
    """Создает продюсера для отправки сообщений"""
    from src.kafka import create_kafka_producer
    # Получаем адрес брокера из контейнера
    bootstrap_server = kafka_container.get_bootstrap_server()
    producer = create_kafka_producer(bootstrap_server)
    yield producer
    producer.close()

@pytest.fixture(scope="module")
def kafka_consumer(kafka_container):
    """Создает консьюмера для чтения сообщений"""
    from src.kafka import create_kafka_consumer
    bootstrap_server = kafka_container.get_bootstrap_server()
    consumer = create_kafka_consumer(bootstrap_server)
    yield consumer
    consumer.close()
