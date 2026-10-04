from dataclasses import dataclass


@dataclass
class Recipe:
    """Рецепт напитка"""
    name: str
    milk_ml: int


class NotEnoughMilkError(Exception):
    """Исключение при нехватке молока"""
    pass


class CoffeeMachine:
    """Кофемашина: выбор напитка и приготовление"""

    # Каталог рецептов
    RECIPES = {
        "Cappuccino": Recipe(name="Cappuccino", milk_ml=50),
        "Espresso": Recipe(name="Espresso", milk_ml=0),
        "Latte": Recipe(name="Latte", milk_ml=150),
    }

    def __init__(self, milk_ml: int = 0):
        self._milk_ml = milk_ml
        self._selected_drink: str | None = None
        self._last_message: str | None = None
        self._brewing_started: bool = False
        self._is_on: bool = True

    @property
    def milk_ml(self) -> int:
        return self._milk_ml

    @property
    def is_ready(self) -> bool:
        return self._is_on

    @property
    def brewing_started(self) -> bool:
        return self._brewing_started

    @property
    def last_message(self) -> str | None:
        return self._last_message

    def select_drink(self, drink: str) -> None:
        if drink not in self.RECIPES:
            raise ValueError(f"Неизвестный напиток: {drink}")
        self._selected_drink = drink

    def press_start(self) -> None:
        """Запускает процесс приготовления. При нехватке ингредиентов — отменяет."""
        if self._selected_drink is None:
            self._last_message = "No drink selected"
            return

        recipe = self.RECIPES[self._selected_drink]

        if self._milk_ml < recipe.milk_ml:
            self._last_message = "Not enough milk"
            self._brewing_started = False
            return

        # Всё в порядке — готовим
        self._milk_ml -= recipe.milk_ml
        self._brewing_started = True
        self._last_message = "Brewing..."