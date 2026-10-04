from behave import given, when, then
from src.cash import ATM, InsufficientFundsError


@given('на счету пользователя "{user}" доступно {amount:d} рублей')
def step_set_balance(context, user, amount):
    context.atm = ATM(balance=amount)
    context.user = user


@given('пользователь успешно авторизован в банкомате')
def step_user_authorized(context):
    assert context.atm.is_authorized()


@when('пользователь запрашивает снятие {amount:d} рублей')
def step_request_withdraw(context, amount):
    try:
        context.withdraw_result = context.atm.withdraw(amount)
        context.withdraw_error = None
    except InsufficientFundsError as e:
        context.withdraw_error = str(e)
        context.withdraw_result = None


@then('банкомат выдает ошибку "{message}"')
def step_check_error_message(context, message):
    assert context.withdraw_error == message, \
        f"Ожидалось '{message}', получено '{context.withdraw_error}'"


@then('транзакция отменяется')
def step_transaction_cancelled(context):
    assert context.atm.last_transaction_status == "failed"


@then('баланс на счету пользователя остается равным {amount:d} рублей')
def step_check_balance_unchanged(context, amount):
    assert context.atm.balance == amount, \
        f"Ожидался баланс {amount}, фактически {context.atm.balance}"