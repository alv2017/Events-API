from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()


class PersonalAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "last_login",
        )
        read_only_fields = ("last_login",)

    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data["password"] = make_password(password)
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        if validated_data.get("password"):
            password = make_password(validated_data.get("password"))
            instance.password = password
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=128)
    is_active = serializers.BooleanField(required=False, default=True)
    is_staff = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        )
        read_only_fields = (
            "id",
            "last_login",
            "date_joined",
        )

    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data["password"] = make_password(password)
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        if validated_data.get("password"):
            password = make_password(validated_data.get("password"))
            instance.password = password
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_superuser = validated_data.get(
            "is_superuser", instance.is_superuser
        )
        instance.save()
        return instance
