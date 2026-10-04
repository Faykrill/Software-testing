from behave import given, when, then
from src.auth import AuthService


@given('существует активный аккаунт с логином "{login}" и верным паролем "{password}"')
def step_create_account(context, login, password):
    context.auth = AuthService()
    context.auth.create_user(login, password)
    context.login = login
    context.correct_password = password


@given('злоумышленник находится на странице входа')
def step_attacker_on_login_page(context):
    assert context.auth is not None


@when('злоумышленник вводит логин "{login}" и неверный пароль {times:d} раза подряд')
def step_wrong_password_attempts(context, login, times):
    for _ in range(times):
        context.auth.try_login(login, "wrong_password")


@then('аккаунт с логином "{login}" переходит в статус "{status}"')
def step_check_account_status(context, login, status):
    actual = context.auth.get_status(login)
    assert actual == status, f"Ожидался статус '{status}', получен '{actual}'"


@then('при следующей попытке входа с верным паролем система выдаёт ошибку "{message}"')
def step_check_blocked_login(context, message):
    result = context.auth.try_login(context.login, context.correct_password)
    assert result == message, f"Ожидалось '{message}', получено '{result}'"