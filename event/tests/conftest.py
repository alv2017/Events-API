from datetime import timedelta

import pytest
from django.utils import timezone

from ..models import Event


@pytest.fixture
def events_data():
    events = {
        "future_event": {
            "name": "Future Event",
            "description": "Event in the future",
            "start": timezone.now() + timedelta(days=1),
            "end": timezone.now() + timedelta(days=1, hours=4),
            "is_published": True,
        },
        "past_event": {
            "name": "Past Event",
            "description": "Event in the past",
            "start": timezone.now() - timedelta(days=1, hours=4),
            "end": timezone.now() - timedelta(days=1),
            "is_published": True,
        },
        "today_event": {
            "name": "Today's Event",
            "description": "Event taking place today",
            "start": timezone.now() + timedelta(seconds=1),
            "end": timezone.now() + timedelta(hours=1),
            "is_published": True,
        },
        "unpublished_event": {
            "name": "Unpublished Event",
            "description": "Event that was not published",
            "start": timezone.now() + timedelta(days=1),
            "end": timezone.now() + timedelta(days=1, hours=1),
            "is_published": False,
        },
    }
    return events


@pytest.fixture
def db_events(test_db_user, events_data):
    events = []
    for event_data in events_data.values():
        event = Event.objects.create(**event_data, arranged_by=test_db_user)
        events.append(event)
    return events


@pytest.fixture
def db_events_of_other(another_test_db_user, events_data):
    events = []
    for event_data in events_data.values():
        event = Event.objects.create(**event_data, arranged_by=another_test_db_user)
        events.append(event)
    return events


@pytest.fixture
def db_events_of_other_with_registrations(
    another_test_db_user, test_db_user, events_data
):
    events = []
    for event_data in events_data.values():
        event = Event.objects.create(**event_data, arranged_by=another_test_db_user)
        event.registrations.add(test_db_user)
        events.append(event)
    return events


@pytest.fixture
def db_events_of_owner_with_registrations(test_db_user, events_data):
    events = []
    for event_data in events_data.values():
        event = Event.objects.create(**event_data, arranged_by=test_db_user)
        event.registrations.add(test_db_user)
        events.append(event)
    return events
