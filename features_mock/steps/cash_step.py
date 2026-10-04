from behave import given, when, then
from features_mock.steps.mock import ATM


@given('на счету пользователя "{user}" доступно {amount:d} рублей')
def step_set_balance(context, user, amount):
    context.atm = ATM(balance=amount)
    context.user = user


@given('пользователь успешно авторизован в банкомате')
def step_user_authorized(context):
    # для данного сценария авторизация — просто формальность
    context.authorized = True


@when('пользователь запрашивает снятие {amount:d} рублей')
def step_request_withdraw(context, amount):
    context.withdraw_result = context.atm.withdraw(amount)


@then('банкомат выдает ошибку "{message}"')
def step_check_error_message(context, message):
    assert context.withdraw_result == message, \
        f"Ожидалось '{message}', получено '{context.withdraw_result}'"


@then('транзакция отменяется')
def step_transaction_cancelled(context):
    assert context.atm.last_transaction_status == "failed"


@then('баланс на счету пользователя остается равным {amount:d} рублей')
def step_check_balance_unchanged(context, amount):
    assert context.atm.balance == amount, \
        f"Ожидался баланс {amount}, фактически {context.atm.balance}"