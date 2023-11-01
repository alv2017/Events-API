import math

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import filters, generics, permissions, status, views, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Event
from .permissions import IsOwner
from .serializers import EventPreviewSerializer, EventSerializer

User = get_user_model()


class EventListCreateView(generics.ListCreateAPIView):
    name = "event_list_create_view"
    serializer_class = EventSerializer
    preview_serializer_class = EventPreviewSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["^start"]
    ordering = ["-start"]

    def get_queryset(self):
        qs = Event.events.all()
        t = self.request.query_params.get("t")
        if t == "today":
            qs = Event.events.today_events()
        elif t == "past":
            qs = Event.events.past_events()
        elif t == "future":
            qs = Event.events.future_events()
        elif t == "all":
            qs = qs
        else:
            qs = Event.events.published_events()
        return qs.select_related("arranged_by").prefetch_related("registrations")

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method == "GET":
            serializer_class = self.preview_serializer_class

        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    name = "event_retrieve_update_destroy_view"
    serializer_class = EventSerializer
    preview_serializer_class = EventPreviewSerializer
    queryset = Event.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsOwner,)
    preview_permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.request.method == "GET":
            permission_classes = self.preview_permission_classes
        return [permission() for permission in permission_classes]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method == "GET":
            serializer_class = self.preview_serializer_class

        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class UserEventsView(generics.ListAPIView):
    name = "user_events_view"
    serializer_class = EventPreviewSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        user = get_object_or_404(User.objects.all(), pk=user_id)
        return (
            user.events.all()
            .select_related("arranged_by")
            .prefetch_related("registrations")
        )


class UserRegistrationsListView(generics.ListAPIView):
    name = "user_registrations_view"
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventPreviewSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        user = get_object_or_404(User.objects.all(), pk=user_id)
        return (
            user.registrations.all()
            .select_related("arranged_by")
            .prefetch_related("registrations")
        )


class UserEventRegistrationView(views.APIView):
    name = "user_event_registration_view"
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventSerializer

    def post(self, args, **kwargs):
        user_id = self.request.user.id
        user = get_object_or_404(User.objects.all(), pk=user_id)
        event_id = self.kwargs["event_id"]
        event = get_object_or_404(Event.objects.all(), pk=event_id)

        # user is already registered for the event
        if user in event.registrations.all():
            message = "You are already registered for this event"
            raise ValidationError(
                detail={"registration error": message},
                code="registration_already_exists",
            )

        # event registration deadline exceeded
        if event.registration_deadline:
            registration_deadline = event.registration_deadline
        else:
            registration_deadline = event.start

        if registration_deadline <= timezone.now():
            message = "Unable to register: event registration is over."
            raise ValidationError(
                detail={"registration error": message}, code="registration_is_over"
            )

        # event is not published
        if not event.is_published:
            message = "Unable to register: event is not published."
            raise ValidationError(
                detail={"registration error": message},
                code="registration_for_unpublished_event",
            )

        # event is fully booked
        seats_available = event.number_of_seats or math.inf
        if event.total_registrations >= seats_available:
            message = "No more registrations accepted, event is fully booked"
            raise ValidationError(
                detail={"registration error": message},
                code="registration_for_fully_booked_event",
            )

        event.registrations.add(user)
        message = f"Your are registered for the event: {event.name}."
        return Response(data={"message": message}, status=status.HTTP_201_CREATED)

    def delete(self, args, **kwargs):
        user_id = self.request.user.id
        user = get_object_or_404(User.objects.all(), pk=user_id)
        event_id = self.kwargs["event_id"]
        event = get_object_or_404(Event.objects.all(), pk=event_id)
        event.registrations.remove(user)
        message = f"Your registration is cancelled: {event.name}."
        return Response(data={"message": message}, status=status.HTTP_204_NO_CONTENT)
