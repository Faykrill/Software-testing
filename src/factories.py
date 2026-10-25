import factory
from .models import Order

class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    # Используем встроенную интеграцию factory-boy с Faker
    # 'sentence' сгенерирует случайное название (например, из 3 слов)
    item_name = factory.Faker('sentence', nb_words=3)
    
    # 'pyint' сгенерирует случайное целое число в заданном диапазоне
    quantity = factory.Faker('pyint', min_value=1, max_value=50)
