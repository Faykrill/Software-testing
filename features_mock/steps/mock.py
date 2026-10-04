class ATM:
    """Имитация банкомата"""
    def __init__(self, balance):
        self.balance = balance
        self.last_transaction_status = None

    def withdraw(self, amount):
        if amount > self.balance:
            self.last_transaction_status = "failed"
            return "Insufficient funds"
        self.balance -= amount
        self.last_transaction_status = "success"
        return "OK"


class AuthSystem:
    """Имитация системы аутентификации"""
    def __init__(self):
        self.users = {}
        self.failed_attempts = {}

    def create_user(self, login, password):
        self.users[login] = {"password": password, "status": "Active"}
        self.failed_attempts[login] = 0

    def try_login(self, login, password):
        user = self.users.get(login)
        if user is None:
            return "User not found"
        if user["status"] == "Blocked":
            return "Account Blocked"
        if user["password"] != password:
            self.failed_attempts[login] += 1
            if self.failed_attempts[login] >= 3:
                user["status"] = "Blocked"
            return "Wrong password"
        # успешный вход — сбрасываем счётчик
        self.failed_attempts[login] = 0
        return "OK"

    def get_status(self, login):
        return self.users[login]["status"]


class CoffeeMachine:
    """Имитация кофемашины"""
    RECIPES = {
        "Cappuccino": {"milk_ml": 50},
        "Espresso": {"milk_ml": 0},
    }

    def __init__(self, milk_ml):
        self.milk_ml = milk_ml
        self.selected_drink = None
        self.last_message = None
        self.brewing_started = False

    def select_drink(self, drink):
        self.selected_drink = drink

    def press_start(self):
        recipe = self.RECIPES.get(self.selected_drink)
        if recipe is None:
            self.last_message = "Unknown drink"
            return
        if self.milk_ml < recipe["milk_ml"]:
            self.last_message = "Not enough milk"
            self.brewing_started = False
            return
        self.milk_ml -= recipe["milk_ml"]
        self.brewing_started = True
        self.last_message = "Brewing..."