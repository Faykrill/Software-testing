from .models import Order

def process_order(db_session, order: Order, kafka_producer):
    """
    Логика сервиса orders: сохранение в БД и отправка события в Kafka
    """
    # 1. Сохраняем заказ в базу данных
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order) # Обновляем объект, чтобы получить сгенерированный ID
    
    # 2. Формируем и отправляем сообщение в Kafka
    message = {
        "id": order.id,
        "item_name": order.item_name,
        "quantity": order.quantity
    }
    
    kafka_producer.send("orders_topic", value=message)
    kafka_producer.flush() # Убеждаемся, что сообщение отправлено на брокер
    
    return order

def process_notifications(kafka_consumer):
    """
    Логика сервиса notifications: чтение событий из Kafka
    """
    received_messages = []
    
    # Используем poll с таймаутом, чтобы не зависнуть, если сообщений нет.
    # Это идеально для интеграционного теста: ждем до 5 секунд.
    records = kafka_consumer.poll(timeout_ms=5000, max_records=10)
    
    for tp, msgs in records.items():
        for msg in msgs:
            # Логгируем информацию о новом заказе
            print(f"[Notification] Получен новый заказ ID={msg.value['id']}: {msg.value['item_name']} ({msg.value['quantity']} шт.)")
            received_messages.append(msg.value)
            
    return received_messages
