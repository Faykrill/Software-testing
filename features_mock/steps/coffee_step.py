from behave import given, when, then
from features_mock.steps.mock import CoffeeMachine


@given('кофемашина включена и готова к работе')
def step_machine_ready(context):
    # сам объект создадим в следующем шаге, где известна температура/молоко
    context.machine_ready = True


@given('в отсеке для молока осталось {milk:d} мл')
def step_set_milk_level(context, milk):
    context.machine = CoffeeMachine(milk_ml=milk)


@given('для приготовления капучино необходимо не менее {required:d} мл молока')
def step_set_recipe_requirement(context, required):
    # в нашем моке рецепт уже зашит (50 мл), но мы можем проверить, что он совпадает
    assert context.machine.RECIPES["Cappuccino"]["milk_ml"] == required


@when('пользователь выбирает напиток "{drink}"')
def step_select_drink(context, drink):
    context.machine.select_drink(drink)


@when('пользователь нажимает кнопку "{button}"')
def step_press_start(context, button):
    assert button == "Start"
    context.machine.press_start()


@then('процесс приготовления не запускается')
def step_brewing_not_started(context):
    assert context.machine.brewing_started is False


@then('система выводит ошибку "{message}"')
def step_check_error(context, message):
    assert context.machine.last_message == message, \
        f"Ожидалось '{message}', получено '{context.machine.last_message}'"