from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView


class LoginView(TokenObtainPairView):
    throttle_scope = "limit_attempts"


class TokenVerificationView(TokenVerifyView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    throttle_scope = "limit_attempts"
