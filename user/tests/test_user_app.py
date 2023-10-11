import pytest
from django.contrib.auth.hashers import check_password
from django.urls import reverse

from ..views import (
    PersonalAccountCreateView,
    PersonalAccountRetrieveUpdateView,
    UserViewSet,
)


class TestPersonalAccountCreateView:
    view = PersonalAccountCreateView
    url = reverse(view.name)

    def test_create_user(self, db, api_client, test_user_data):
        response = api_client.post(path=self.url, data=test_user_data, format="json")
        assert response.status_code == 201
        assert response.data["username"] == test_user_data["username"]
        assert "password" not in response.data


class TestPersonalAccountRetrieveUpdateView:
    view = PersonalAccountRetrieveUpdateView
    url = reverse(view.name)

    def test_retrieve_account_data_unauth_access_is_not_allowed(self, api_client):
        response = api_client.get(path=self.url)
        assert response.status_code == 401

    def test_retrieve_account_data(self, test_db_user, user_api_client):
        api_client = user_api_client
        response = api_client.get(path=self.url)
        assert response.status_code == 200
        user_data = response.data
        assert user_data["username"] == test_db_user.username

    def test_update_account_unauth_access(self, api_client):
        response = api_client.patch(path=self.url, data={})
        assert response.status_code == 401

    def test_update_account_auth_access(self, user_api_client):
        api_client = user_api_client
        response = api_client.patch(path=self.url, data={})
        assert response.status_code == 200

    def test_update_account(
        self, django_user_model, test_db_user, user_api_client, updated_user_data
    ):
        api_client = user_api_client

        # Before update
        user = django_user_model.objects.get(pk=test_db_user.id)
        assert updated_user_data["first_name"] != user.first_name
        assert updated_user_data["last_name"] != user.last_name
        assert updated_user_data["email"] != user.email
        assert not check_password(updated_user_data["password"], user.password)

        # Update
        response = api_client.patch(self.url, updated_user_data)
        assert response.status_code == 200

        # DB data after update
        user = django_user_model.objects.get(pk=test_db_user.id)
        assert updated_user_data["first_name"] == user.first_name
        assert updated_user_data["last_name"] == user.last_name
        assert updated_user_data["email"] == user.email
        assert check_password(updated_user_data["password"], user.password)

    def test_update_account_username_cant_be_updated(
        self, test_db_user, user_api_client, django_user_model
    ):
        new_username = "new_user_name"
        api_client = user_api_client

        # Before update
        user = django_user_model.objects.get(pk=test_db_user.id)
        assert user.username != new_username
        db_user_name = user.username

        # Update attempt
        response = api_client.patch(self.url, {"username": new_username})
        assert response.status_code == 200

        # DB data after update: username can not be updated
        user = django_user_model.objects.get(pk=1)
        assert user.username == db_user_name
        assert new_username != user.username


class TestUserManagementViews:
    user_list_create_view_name = "user_list_create_view"
    user_list_create_view_url = reverse(user_list_create_view_name)
    user_retrieve_update_delete_view_name = "user_retrieve_update_delete_view"

    def user_retrieve_update_delete_view_url(self, pk: int):
        return reverse(self.user_retrieve_update_delete_view_name, kwargs={"pk": pk})

    def test_user_list_view_unauthorized_access_is_not_allowed(self, api_client):
        response = api_client.get(self.user_list_create_view_url)
        assert response.status_code == 401

    def test_user_list_view_regular_user_access_is_forbidden(self, user_api_client):
        api_client = user_api_client
        response = api_client.get(self.user_list_create_view_url)
        assert response.status_code == 403

    def test_user_list_view_admin_access(self, admin_api_client):
        api_client = admin_api_client
        response = api_client.get(self.user_list_create_view_url)
        assert response.status_code == 200

    def test_user_create_view_unauthorized_access_is_not_allowed(
        self, api_client, test_user_data
    ):
        response = api_client.post(self.user_list_create_view_url, data=test_user_data, format="json")
        assert response.status_code == 401

    def test_user_create_view_regular_user_access_is_forbidden(self, user_api_client, test_user_data):
        api_client = user_api_client
        response = api_client.post(self.user_list_create_view_url, data=test_user_data, format="json")
        assert response.status_code == 403

    def test_user_create_view_admin_access(self, admin_api_client, test_user_data):
        api_client = admin_api_client
        response = api_client.post(self.user_list_create_view_url, data=test_user_data, format="json")
        created_user = response.data
        assert response.status_code == 201
        assert created_user["username"] == test_user_data["username"]
        assert created_user["email"] == test_user_data["email"]

    def test_user_details_view_unauthorized_access_is_not_allowed(self, api_client):
        response = api_client.get(self.user_retrieve_update_delete_view_url(1))
        assert response.status_code == 401

    def test_user_details_view_regular_user_access_is_forbidden(self, user_api_client):
        api_client = user_api_client
        response = api_client.get(self.user_retrieve_update_delete_view_url(1))
        assert response.status_code == 403

    def test_user_details_view_admin_access(self, admin_api_client):
        api_client = admin_api_client
        response = api_client.get(self.user_retrieve_update_delete_view_url(1))
        assert response.status_code == 200

    def test_user_update_view_unauthorized_access_is_not_allowed(self, api_client):
        response = api_client.put(self.user_retrieve_update_delete_view_url(1), data={}, format="json")
        assert response.status_code == 401

    def test_user_update_view_regular_user_access_is_forbidden(self, user_api_client):
        api_client = user_api_client
        response = api_client.put(self.user_retrieve_update_delete_view_url(1), data={}, format="json")
        assert response.status_code == 403

    def test_user_update_view_admin_access(self, admin_api_client):
        api_client = admin_api_client
        response = api_client.put(self.user_retrieve_update_delete_view_url(1), data={}, format="json")
        assert response.status_code == 200

    def test_user_update_view_with_data(self, admin_api_client, test_db_user, updated_user_data, django_user_model):
        api_client = admin_api_client
        updated_user_data["username"] = "updated_user_name"
        user_id = test_db_user.id

        # Before update
        user = django_user_model.objects.get(pk=user_id)
        assert user.username != updated_user_data["username"]
        assert user.first_name != updated_user_data["first_name"]
        assert user.last_name != updated_user_data["last_name"]
        assert user.email != updated_user_data["email"]
        assert not check_password(updated_user_data["password"], user.password)

        # Update
        response = api_client.put(self.user_retrieve_update_delete_view_url(test_db_user.id),
                                  data=updated_user_data, format="json")
        assert response.status_code == 200

        # DB data after update
        user = django_user_model.objects.get(pk=user_id)
        assert user.username == updated_user_data["username"]
        assert user.first_name == updated_user_data["first_name"]
        assert user.last_name == updated_user_data["last_name"]
        assert user.email == updated_user_data["email"]
        assert check_password(updated_user_data["password"], user.password)

    def test_user_delete_view_unauthorized_access_is_not_allowed(self, api_client, test_db_user):
        response = api_client.delete(self.user_retrieve_update_delete_view_url(test_db_user.id))
        assert response.status_code == 401

    def test_user_delete_view_regular_user_access_is_forbidden(self, user_api_client):
        api_client = user_api_client
        response = api_client.delete(self.user_retrieve_update_delete_view_url(1))
        assert response.status_code == 403

    def test_user_delete_view_admin_access(self, admin_api_client, test_db_user):
        api_client = admin_api_client
        response = api_client.delete(self.user_retrieve_update_delete_view_url(test_db_user.id))
        assert response.status_code == 204
