from dataclasses import dataclass, field


class AccountBlockedError(Exception):
    """Исключение при заблокированном аккаунте"""
    pass


@dataclass
class UserAccount:
    """Модель учётной записи пользователя"""
    login: str
    password: str
    status: str = "Active"
    failed_attempts: int = 0

    MAX_ATTEMPTS = 3


class AuthService:
    """Сервис аутентификации: регистрация, вход, блокировка"""

    def __init__(self):
        self._users: dict[str, UserAccount] = {}

    def create_user(self, login: str, password: str) -> UserAccount:
        if login in self._users:
            raise ValueError(f"Пользователь {login} уже существует")
        user = UserAccount(login=login, password=password)
        self._users[login] = user
        return user

    def try_login(self, login: str, password: str) -> str:
        """
        Попытка входа.
        Возвращает строку-результат: 'OK', 'Wrong password', 'Account Blocked', 'User not found'.
        """
        user = self._users.get(login)
        if user is None:
            return "User not found"

        if user.status == "Blocked":
            return "Account Blocked"

        if user.password != password:
            user.failed_attempts += 1
            if user.failed_attempts >= UserAccount.MAX_ATTEMPTS:
                user.status = "Blocked"
            return "Wrong password"

        # Успешный вход — сбрасываем счётчик неудачных попыток
        user.failed_attempts = 0
        return "OK"

    def get_status(self, login: str) -> str:
        user = self._users.get(login)
        if user is None:
            raise ValueError(f"Пользователь {login} не найден")
        return user.status