import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def test_user_data() -> dict:
    user_data = {
        "username": "test_user",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email@test.com",
        "password": "test_password",
    }
    return user_data


@pytest.fixture(scope="function")
def test_db_user(django_user_model, test_user_data) -> User:
    try:
        user = django_user_model.objects.get(username=test_user_data["username"])
    except django_user_model.DoesNotExist:
        user = django_user_model.objects.create_user(**test_user_data)
    return user


@pytest.fixture
def user_api_client(api_client, test_db_user):
    client = api_client
    refresh = RefreshToken.for_user(test_db_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def another_test_user_data() -> dict:
    user_data = {
        "username": "another_user",
        "first_name": "another_first_name",
        "last_name": "another_last_name",
        "email": "another_email@test.com",
        "password": "antother_test_password",
    }
    return user_data


@pytest.fixture(scope="function")
def another_test_db_user(django_user_model, another_test_user_data) -> User:
    try:
        user = django_user_model.objects.get(username=another_test_user_data["username"])
    except django_user_model.DoesNotExist:
        user = django_user_model.objects.create(**another_test_user_data)
    return user


@pytest.fixture
def admin_user_data() -> dict:
    user_data = {
        "username": "test_admin",
        "first_name": "admin_first_name",
        "last_name": "admin_last_name",
        "email": "admin_email@test.com",
        "password": "admin_test_password",
        "is_staff": True,
        "is_superuser": False,
    }
    return user_data


@pytest.fixture
def db_admin_user(db, django_user_model, admin_user_data):
    try:
        admin_user = django_user_model.objects.get(username=admin_user_data["username"])
    except django_user_model.DoesNotExist:
        admin_user = django_user_model.objects.create_user(**admin_user_data)
    return admin_user


@pytest.fixture
def admin_api_client(api_client, db_admin_user):
    client = api_client
    refresh = RefreshToken.for_user(db_admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
