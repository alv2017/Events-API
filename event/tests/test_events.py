import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.fields import DateTimeField

from ..models import Event
from ..views import (
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    UserEventRegistrationView,
    UserEventsView,
    UserRegistrationsListView,
)

drf_string_to_datetime = DateTimeField().to_internal_value
drf_datetime_to_string = DateTimeField().to_representation


class TestEventListCreateView:
    view = EventListCreateView
    url = reverse(view.name)

    def test_event_list_view_unauth_access_is_not_allowed(self, api_client):
        response = api_client.get(path=self.url)
        assert response.status_code == 401

    def test_event_list_view(self, user_api_client):
        api_client = user_api_client
        response = api_client.get(path=self.url)
        assert response.status_code == 200

    def test_event_list_displays_only_published_events(
        self, user_api_client, db_events
    ):
        api_client = user_api_client
        response = api_client.get(path=self.url)
        assert response.status_code == 200
        for event in response.data:
            assert event["is_published"]

    def test_event_list_query_parameter_t_past(self, user_api_client, db_events):
        user_api_client = user_api_client
        response = user_api_client.get(self.url, {"t": "past"})
        assert response.status_code == 200
        for event in response.data:
            event_time = drf_string_to_datetime(event["start"])
            assert event_time < timezone.now()

    def test_event_list_query_parameter_t_today(self, user_api_client, db_events):
        user_api_client = user_api_client
        response = user_api_client.get(self.url, {"t": "today"})
        assert response.status_code == 200
        for event in response.data:
            event_time = drf_string_to_datetime(event["start"])
            assert event_time.date() == timezone.now().date()

    def test_event_list_query_parameter_t_future(self, user_api_client, db_events):
        user_api_client = user_api_client
        response = user_api_client.get(self.url, {"t": "future"})
        assert response.status_code == 200
        for event in response.data:
            event_time = drf_string_to_datetime(event["start"])
            assert event_time > timezone.now()

    def test_event_create_view_unauth_access_is_not_allowed(self, api_client):
        response = api_client.post(self.url, data={})
        assert response.status_code == 401

    def test_event_create_view(self, user_api_client, events_data):
        api_client = user_api_client
        # Before create
        assert Event.objects.count() == 0

        cnt = 0
        for event_data in events_data.values():
            response = api_client.post(self.url, data=event_data)
            assert response.status_code == 201
            cnt += 1
            assert Event.objects.count() == cnt


class TestEventRetrieveUpdatedDestroyView:
    view = EventRetrieveUpdateDestroyView

    def get_url(self, event_id: int):
        return reverse(self.view.name, kwargs={"pk": event_id})

    def test_event_retrieve_view_unauth_access_is_not_allowed(self, api_client):
        url = self.get_url(event_id=1)
        response = api_client.get(url)
        assert response.status_code == 401

    def test_event_retrieve_view(self, user_api_client, db_events):
        event_id = 1
        url = self.get_url(event_id=event_id)
        api_client = user_api_client
        response = api_client.get(url)
        assert response.status_code == 200
        event_data = response.data
        assert event_data["id"] == event_id

    def test_event_update_view_unauth_access_is_not_allowed(self, api_client):
        url = self.get_url(event_id=1)
        response = api_client.put(url)
        assert response.status_code == 401
        response = api_client.patch(url)
        assert response.status_code == 401

    def test_event_update_view_modification_of_events_of_others_is_not_allowed(
        self, test_db_user, another_test_db_user, db_events_of_other, user_api_client
    ):
        api_client = user_api_client
        # Event that we will try to update
        event_id = 1
        event = Event.objects.get(pk=1)
        assert event.arranged_by == another_test_db_user
        assert test_db_user != another_test_db_user

        # Event update attempt
        url = self.get_url(event_id=event_id)
        response = api_client.patch(url, data={"name": "Test DB User Event"})
        assert response.status_code == 403

    def test_event_update_view(self, user_api_client, db_events):
        # Before update
        event_id = 1
        event = Event.objects.get(pk=event_id)
        new_name = "New Event Name"
        assert event.name != new_name

        # Event update
        url = self.get_url(event_id=event_id)
        api_client = user_api_client
        response = api_client.patch(url, data={"name": new_name})
        assert response.status_code == 200
        event_data = response.data

        # After update
        event = Event.objects.get(pk=event_id)
        assert event.id == event_id
        assert event.name == new_name

    def test_event_delete_view_unauth_access_is_not_allowed(self, api_client):
        url = self.get_url(event_id=1)
        response = api_client.delete(url)
        assert response.status_code == 401

    def test_event_delete_view_deletion_of_events_of_others_is_not_allowed(
        self, test_db_user, another_test_db_user, db_events_of_other, user_api_client
    ):
        api_client = user_api_client

        # Event that we will try to delete
        event_id = 1
        event = Event.objects.get(pk=1)
        assert event.arranged_by == another_test_db_user
        assert test_db_user != another_test_db_user

        # Delete attempt
        url = self.get_url(event_id=1)
        response = api_client.delete(url)
        assert response.status_code == 403

    def test_event_delete_view(self, test_db_user, user_api_client, db_events):
        api_client = user_api_client

        # Event to be deleted
        event_id = 1
        event = Event.objects.get(pk=1)
        assert event.arranged_by == test_db_user

        # Delete event
        url = self.get_url(event_id=event_id)
        response = api_client.delete(url)
        assert response.status_code == 204
        with pytest.raises(Event.DoesNotExist):
            Event.objects.get(pk=1)


class TestUserEventsView:
    view = UserEventsView
    url = reverse(view.name)

    def test_user_events_view_unauth_access_is_not_allowed(self, api_client):
        response = api_client.get(path=self.url)
        assert response.status_code == 401

    def test_user_events_view_no_events_created(self, test_db_user, user_api_client):
        assert Event.objects.count() == 0
        api_client = user_api_client
        response = api_client.get(path=self.url)
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_user_events_view_with_user_created_events(
        self, test_db_user, user_api_client, db_events
    ):
        n = Event.objects.filter(arranged_by=test_db_user).count()
        assert n > 0
        api_client = user_api_client
        response = api_client.get(path=self.url)
        assert response.status_code == 200
        assert len(response.data) > 0
        assert len(response.data) == n
        for event in response.data:
            assert event["arranged_by"] == test_db_user.id


class TestUserRegistrationsListView:
    view = UserRegistrationsListView
    url = reverse(view.name)

    def test_user_registrations_list_view_unauth_access_is_not_allowed(
        self, api_client
    ):
        response = api_client.get(self.url)
        assert response.status_code == 401

    def test_user_registrations_list_is_empty(self, user_api_client):
        api_client = user_api_client
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_user_registrations_list_not_empty(
        self,
        another_test_db_user,
        test_db_user,
        db_events_of_other_with_registrations,
        user_api_client,
    ):
        api_client = user_api_client
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert len(response.data) != 0
        for event in response.data:
            assert test_db_user.id in event["registrations"]


class TestUserEventRegistrationView:
    view = UserEventRegistrationView

    def get_url(self, event_id: int):
        return reverse(self.view.name, kwargs={"event_id": event_id})

    def test_event_registration_view_unauth_access_is_not_allowed(self, api_client):
        url = self.get_url(event_id=1)
        response = api_client.post(url, data={})
        assert response.status_code == 401

    def test_registration_for_event_arranged_by_me(
        self, test_db_user, db_events, user_api_client
    ):
        api_client = user_api_client
        # Before registration
        event_id = 1
        event = Event.objects.get(pk=event_id)
        assert event.registrations.count() == 0

        # Registration for event
        url = self.get_url(event_id=1)
        response = api_client.post(url, data={})
        assert response.status_code == 201

        # After registration
        event = Event.objects.get(pk=event_id)
        assert event.registrations.count() == 1
        assert test_db_user in event.registrations.all()

    def test_register_for_event_arranged_by_other(
        self, test_db_user, another_test_db_user, db_events_of_other, user_api_client
    ):
        api_client = user_api_client

        # Before registration
        event_id = 1
        event = Event.objects.get(pk=event_id)
        assert event.registrations.count() == 0
        assert event.arranged_by == another_test_db_user
        assert test_db_user != another_test_db_user

        # Registration for event
        url = self.get_url(event_id=1)
        response = api_client.post(url, data={})
        assert response.status_code == 201

        # After the registration
        event = Event.objects.get(pk=event_id)
        assert event.registrations.count() == 1
        assert test_db_user in event.registrations.all()

    def test_cancel_registration_for_event_unauth_access_is_not_allowed(
        self, api_client
    ):
        url = self.get_url(event_id=1)
        response = api_client.delete(url)
        assert response.status_code == 401

    def test_cancel_registration_for_event_arranged_by_me(
        self, test_db_user, user_api_client, db_events_of_owner_with_registrations
    ):
        api_client = user_api_client

        # Before registration cancellation
        event_id = 1
        event = Event.objects.get(pk=event_id)
        assert test_db_user in event.registrations.all()

        # Cancel registration
        url = self.get_url(event_id=event_id)
        response = api_client.delete(url)
        assert response.status_code == 204

        # After the cancellation
        event = Event.objects.get(pk=event_id)
        assert test_db_user not in event.registrations.all()

    def test_cancel_registration_for_event_arranged_by_other(
        self,
        test_db_user,
        another_test_db_user,
        user_api_client,
        db_events_of_other_with_registrations,
    ):
        api_client = user_api_client

        # Before registration cancellation
        event_id = 1
        event = Event.objects.get(pk=event_id)
        assert event.arranged_by == another_test_db_user
        assert test_db_user in event.registrations.all()

        # Cancel registration
        url = self.get_url(event_id=event_id)
        response = api_client.delete(url)
        assert response.status_code == 204

        # After the cancellation
        event = Event.objects.get(pk=event_id)
        assert test_db_user not in event.registrations.all()
