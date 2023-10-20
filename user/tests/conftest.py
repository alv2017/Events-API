import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def updated_user_data(django_user_model) -> dict:
    user_data = {
        "first_name": "updated_first_name",
        "last_name": "updated_last_name",
        "email": "updated_email@test.com",
        "password": "updated_password",
    }
    return user_data
