class InsufficientFundsError(Exception):
    """Исключение при нехватке средств"""
    pass


class ATM:
    """Банкомат: хранит баланс и выполняет операции снятия"""

    def __init__(self, balance: float = 0.0):
        self._balance = balance
        self._last_transaction_status = None

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def last_transaction_status(self) -> str | None:
        return self._last_transaction_status

    def withdraw(self, amount: float) -> str:
        """
        Пытается снять указанную сумму.
        Возвращает строку-результат (для совместимости с нашим сценарием).
        При нехватке средств транзакция отменяется.
        """
        if amount > self._balance:
            self._last_transaction_status = "failed"
            raise InsufficientFundsError("Insufficient funds")

        self._balance -= amount
        self._last_transaction_status = "success"
        return "OK"

    def is_authorized(self) -> bool:
        """Упрощённая проверка авторизации"""
        return True