from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, TokenVerificationView

urlpatterns = [
    path("login/", LoginView.as_view(), name="token_obtain"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerificationView.as_view(), name="token_verify"),
]
