from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = "auth"
    label = "auth_token"

    def ready(self):
        import auth.signals
