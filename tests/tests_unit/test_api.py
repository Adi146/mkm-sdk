import pytest

from oauthlib.oauth1 import Client

from mkmsdk.MKMClient import MKMClient
from mkmsdk.api import Api
from mkmsdk import exceptions
from mkmsdk.utils import get_mkm_app_secret


def test_create_auth():
    """
    Verifies that the default Client is used
    when all the tokens are not empty strings.
    """
    api = Api("https://api.cardmarket.com/ws/v1.1/output.json")
    auth = api.create_auth(
        "https://api.cardmarket.com/ws/v1.1/output.json",
        app_token="app_token",
        app_secret="app_secret",
        access_token="access_token",
        access_token_secret="access_token_secret",
    )

    assert isinstance(auth.client, Client)
    assert auth.client.client_key == "app_token"
    assert auth.client.client_secret == "app_secret"
    assert auth.client.resource_owner_key == "access_token"
    assert auth.client.resource_owner_secret == "access_token_secret"


def test_create_auth_with_empty_string_token():
    """
    Verifies that the custom MKMClient is used
    when access token and access token secret
    are empty strings.
    """
    api = Api("https://api.cardmarket.com/ws/v1.1/output.json")
    auth = api.create_auth(
        "https://api.cardmarket.com/ws/v1.1/output.json",
        app_token="app_token",
        app_secret="app_secret",
        access_token="",
        access_token_secret="",
    )

    assert isinstance(auth.client, MKMClient)
    assert auth.client.client_key == "app_token"
    assert auth.client.client_secret == "app_secret"
    assert auth.client.resource_owner_key == ""
    assert auth.client.resource_owner_secret == ""


def test_missing_env_var_raise_exception_correctly(mocker):
    """Verifies that an expection is thrown when necessary env vars are missing."""
    os_mocked = mocker.patch("mkmsdk.utils.os")
    os_mocked.environ = {}
    with pytest.raises(exceptions.MissingEnvVar):
        get_mkm_app_secret()


def test_endpoint():
    """Verifies the live endpoint is used by default."""
    api = Api("https://api.cardmarket.com/ws/v1.1/output.json")
    expected_live_base_endpoint = "https://api.cardmarket.com/ws/v1.1/output.json"

    assert api.base_endpoint == expected_live_base_endpoint


def test_sandbox_mode():
    """Verifies the sandbox endpoint is used when specified."""
    sandbox_api = Api("https://sandbox.cardmarket.com/ws/v1.1/output.json")
    expected_sandbox_base_endpoint = "https://sandbox.cardmarket.com/ws/v1.1/output.json"

    assert sandbox_api.base_endpoint == expected_sandbox_base_endpoint


def test_handle_request(mocked_response):
    api = Api("https://sandbox.cardmarket.com/ws/v1.1/output.json")

    mocked_response.status_code = 400
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 401
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 403
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 404
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 405
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 409
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 410
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 422
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 480
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 545
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)

    mocked_response.status_code = 1001
    with pytest.raises(exceptions.ConnectionError):
        api.handle_response(mocked_response)


def test_request_with_auth_params(mocker):
    mocker.patch("mkmsdk.api.request")
    api = Api("https://sandbox.cardmarket.com/ws/v1.1/output.json")
    mocker.patch.object(api, 'create_auth')
    mocker.patch.object(api, 'handle_response')

    auth_params = {
        "app_token": "my_app_token",
        "app_secret": "my_app_secret",
        "access_token": "my_access_token",
        "access_token_secret": "my_access_token_secret"
    }

    api.request("/games", "get", auth_params=auth_params)

    api.create_auth.assert_called_with(
        "https://sandbox.cardmarket.com/ws/v1.1/output.json/games",
        app_token="my_app_token",
        app_secret="my_app_secret",
        access_token="my_access_token",
        access_token_secret="my_access_token_secret"
    )
