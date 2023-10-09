from django.urls import path

from .views import (
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    UserEventRegistrationView,
    UserEventsView,
    UserRegistrationsListView,
)

urlpatterns = [
    path("events/", EventListCreateView.as_view(), name=EventListCreateView.name),
    path(
        "events/<int:pk>/",
        EventRetrieveUpdateDestroyView.as_view(),
        name=EventRetrieveUpdateDestroyView.name,
    ),
    path("me/events/", UserEventsView.as_view(), name=UserEventsView.name),
    path(
        "me/registrations/",
        UserRegistrationsListView.as_view(),
        name=UserRegistrationsListView.name,
    ),
    path(
        "me/registrations/<int:event_id>/",
        UserEventRegistrationView.as_view(),
        name=UserEventRegistrationView.name,
    ),
]
