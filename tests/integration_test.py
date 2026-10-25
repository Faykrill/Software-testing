from src.factories import OrderFactory
from src.models import Order
from src.services import process_order, process_notifications

def test_full_integration_flow(db_session, kafka_producer, kafka_consumer):
    """
    Тестирует взаимодействие сервисов:
    1. Создание заказа (через фабрику)
    2. Сохранение в БД и отправка в Kafka (сервис orders)
    3. Проверка данных в БД
    4. Чтение из Kafka (сервис notifications)
    5. Проверка корректности сообщения
    """
    
    # 1. С помощью фабрики создаем объект заказа (без хардкода)
    order = OrderFactory()
    
    # 2. Вызываем функцию сервиса orders
    processed_order = process_order(db_session, order, kafka_producer)
    
    # 3. Убеждаемся, что в БД есть корректная запись о заказе
    db_order = db_session.query(Order).filter(Order.id == processed_order.id).first()
    assert db_order is not None
    assert db_order.item_name == order.item_name
    assert db_order.quantity == order.quantity
    
    # 4. Вызываем функцию сервиса notifications
    messages = process_notifications(kafka_consumer)
    
    # 5. Убеждаемся, что полученное сообщение корректно
    assert len(messages) > 0, "Сообщение не было получено из Kafka"
    
    received_message = messages[0]
    
    # Проверяем, что сообщение содержит id и item_name отправленного заказа
    assert received_message["id"] == processed_order.id
    assert received_message["item_name"] == processed_order.item_name
    assert received_message["quantity"] == processed_order.quantity
    