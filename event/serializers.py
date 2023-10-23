from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Event

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=1024, required=False)
    arranged_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    registration_deadline = serializers.DateTimeField(required=False)
    is_published = serializers.BooleanField(required=False, default=True)
    created_on = serializers.DateTimeField(required=False)
    updated_on = serializers.DateTimeField(required=False)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "start",
            "end",
            "arranged_by",
            "registration_deadline",
            "is_published",
            "created_on",
            "updated_on",
        )
        read_only_fields = ("id", "arranged_by", "created_on", "updated_on")


class EventPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
