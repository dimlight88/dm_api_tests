from json import loads
import time

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)


def test_put_v1_account_email():
    # Регистрация пользователя

    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    login = 'dm_qa_put128'
    password = '987654321'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)

    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    # Получаем письма из почтового сервера для активации аккаунта

    response = mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, "Письма не были получены"

    # Из писем извлекаем токен активации регистрации

    token = get_activation_token_by_login(login, response)

    time.sleep(3)

    # Активация аккаунта

    response = account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # Меняем email

    email2 = f'{login}_new@mail.ru'
    json_data = {
        'login': login,
        'password': password,
        'email': email2,
    }
    response = account_api.put_v1_account_email(json_data=json_data)

    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # Пытаемся авторизоваться – получаем 403

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 403, "Пользователь не смог авторизоваться"

    # Смотрим еще раз письма

    response = mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, "Письма не были получены"

    # Из писем извлекаем токен подтверждения смены email

    token = get_activation_token_by_login(login, response)

    time.sleep(3)

    # Активируем новый токен

    response = account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, "Пользователь не был активирован"

    # Логинимся

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, "Пользователь не смог авторизоваться"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
