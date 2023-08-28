import json
import pytest
import logging
from faker import Faker
from jsonschema import validate
from src.api.path import Path
from src.api.request import Request
from src.web.locators import Locators
from src.schemes.get_single_user_successful_scheme import GET_SINGLE_USER_SUCCESSFUL_SCHEME
from src.schemes.get_user_list_successful_scheme import GET_USER_LIST_SUCCESSFUL_SCHEME
from src.schemes.get_unknown_single_successful_scheme import GET_UNKNOWN_SINGLE_SUCCESSFUL_SCHEME
from src.schemes.post_user_response import POST_USER_SUCCESSFUL_SCHEME
from src.schemes.put_user_successful_scheme import PUT_USER_SUCCESSFUL_SCHEME
from src.schemes.get_unknown_list_successful_scheme import GET_UNKNOWN_LIST_SUCCESSFUL_SCHEME
from src.schemes.post_register_successful_scheme import POST_REGISTER_SUCCESSFUL_SCHEME
from src.schemes.post_login_unsuccessful import POST_LOGIN_UNSUCCESSFUL_SCHEME
from src.schemes.post_login_successful import POST_LOGIN_SUCCESSFUL_SCHEME
from src.web.get_response_from_web_page import get_response_from_web_page

faker = Faker()
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

@pytest.mark.parametrize("path,method,query_params,data,scheme,is_negative, expected_status_code, locator, is_response_equal", [
    (Path.USERS, 'get', 'page=1', {}, GET_USER_LIST_SUCCESSFUL_SCHEME, False, 200, Locators.USER_LIST_BUTTON, False),
    (Path.USERS, 'get', 'page=2', {}, GET_USER_LIST_SUCCESSFUL_SCHEME, False, 200, Locators.USER_LIST_BUTTON, True),
    (Path.USERS, 'get', 'delay=3', {}, GET_USER_LIST_SUCCESSFUL_SCHEME, False, 200, Locators.DELAY_BUTTON, True),
    (f'{Path.USERS}/2', 'get', '', {}, GET_SINGLE_USER_SUCCESSFUL_SCHEME, False, 200, Locators.SINGLE_USER_BUTTON, True),
    (f'{Path.USERS}/1', 'get', '', {}, GET_SINGLE_USER_SUCCESSFUL_SCHEME, False, 200, Locators.SINGLE_USER_BUTTON, False),
    (f'{Path.USERS}/1000', 'get', '', {}, GET_SINGLE_USER_SUCCESSFUL_SCHEME, True, 404, Locators.SINGLE_USER_NOT_FOUNDED_BUTTON, False),
    (f'{Path.USERS}/ooo', 'get', '', {}, GET_SINGLE_USER_SUCCESSFUL_SCHEME, True, 404, Locators.SINGLE_USER_NOT_FOUNDED_BUTTON, False),
    (f'{Path.USERS}/23', 'get', '', {}, GET_SINGLE_USER_SUCCESSFUL_SCHEME, False, 404, Locators.SINGLE_USER_NOT_FOUNDED_BUTTON, True),
    (Path.USERS, 'post', '', {'name': faker.name(), 'job': faker.job()}, POST_USER_SUCCESSFUL_SCHEME, False, 201, Locators.POST_BUTTON, False),
    (f'{Path.USERS}/1', 'put', '', {'name': faker.name(), 'job': faker.job()}, PUT_USER_SUCCESSFUL_SCHEME, False, 200, Locators.PUT_BUTTON, False),
    (f'{Path.USERS}/2', 'put', '', {'name': faker.name(), 'job': faker.job()}, PUT_USER_SUCCESSFUL_SCHEME, False, 200, Locators.PUT_BUTTON, False),
    (f'{Path.USERS}/23', 'put', '', {'name': faker.name(), 'job': faker.job()}, PUT_USER_SUCCESSFUL_SCHEME, False, 200, Locators.PUT_BUTTON, False),
    (f'{Path.USERS}/1', 'delete', '', {}, {}, False, 204, Locators.DELETE_BUTTON, False),
    (f'{Path.USERS}/2', 'delete', '', {}, {}, False, 204, Locators.DELETE_BUTTON, True),
    (f'{Path.USERS}/-1', 'delete', '', {}, {}, False, 404, Locators.DELETE_BUTTON, False),
    (f'{Path.USERS}/qwerty', 'delete', '', {}, {}, False, 404, Locators.DELETE_BUTTON, False),
    (Path.LOGIN, 'post', '', {"email": 'eve.holt@reqres.in', 'password': 'cityslicka'}, POST_LOGIN_SUCCESSFUL_SCHEME, False, 200, Locators.LOGIN_SUCCESSFUL_BUTTON, True),
    (Path.LOGIN, 'post', '', {'email': 'peter@klaven'}, POST_LOGIN_UNSUCCESSFUL_SCHEME, False, 400, Locators.LOGIN_UNSUCCESSFUL_BUTTON, False),
    (Path.LOGIN, 'post', '', {}, POST_LOGIN_UNSUCCESSFUL_SCHEME, False, 400, Locators.LOGIN_UNSUCCESSFUL_BUTTON, False),
    (Path.REGISTER, 'post', '', {'email': 'eve.holt@reqres.in', 'password': 'pistol'}, POST_REGISTER_SUCCESSFUL_SCHEME, False, 200, Locators.REGISTER_SUCCESSFUL_BUTTON, True),
    (Path.REGISTER, 'post', '', {'email': 'sydney@fife'}, POST_LOGIN_UNSUCCESSFUL_SCHEME, False, 400, Locators.REGISTER_UNSUCCESSFUL_BUTTON, False),
    (Path.UNKNOWN, 'get', '', {}, GET_UNKNOWN_LIST_SUCCESSFUL_SCHEME, False, 200, Locators.UNKNOWN_BUTTON, False),
    (f'{Path.UNKNOWN}/2', 'get', '', {}, GET_UNKNOWN_SINGLE_SUCCESSFUL_SCHEME, False, 200, Locators.UNKNOWN_SINGLE_BUTTON, True),
    (f'{Path.UNKNOWN}/3', 'get', '', {}, GET_UNKNOWN_SINGLE_SUCCESSFUL_SCHEME, False, 200, Locators.UNKNOWN_SINGLE_BUTTON, False),
    (f'{Path.UNKNOWN}/23', 'get', '', {}, {}, False, 404, Locators.UNKNOWN_SINGLE_NOT_FOUND_BUTTON, True),
])
def test_reqres_api(
        path, method, query_params, data,
        scheme, is_negative, expected_status_code,
        locator, is_response_equal):

    if method == 'get':
        response = Request.get(path, params=query_params)
        if is_negative:
            negative_case(response)
        else:
            positive_case(response, expected_status_code, locator, is_response_equal, scheme)



    if method == 'post':
        response = Request.post(path, data=data)

        if is_negative:
            negative_case(response)
        else:
            positive_case(response, expected_status_code, locator, is_response_equal, scheme)


    if method == 'put':
        response = Request.put(path, data=data)
        if is_negative:
            negative_case(response)
        else:
            positive_case(response, expected_status_code, locator, is_response_equal, scheme)


    if method == 'delete':
        response = Request.delete(path)
        assert response.status_code == expected_status_code


def positive_case(response, expected_status_code, locator, is_response_equal, scheme={}):

    assert response.status_code == expected_status_code
    assert validate(instance=response.json(), schema=scheme) == None


    web_page_status_code, web_page_text = get_response_from_web_page(locator=locator)
    web_page_text_json = json.loads(web_page_text)
    assert int(web_page_status_code) == response.status_code


    if is_response_equal:
       assert web_page_text_json == response.json()


def negative_case(response, scheme={}):
    assert response.status_code == 404
    assert validate(instance=response.json(), schema=scheme) == None
