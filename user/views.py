from django.contrib.auth import get_user_model
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import PersonalAccountSerializer, UserSerializer

User = get_user_model()


class PersonalAccountCreateView(generics.CreateAPIView):
    name = "personal_account_create"
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = PersonalAccountSerializer


class PersonalAccountRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    name = "personal_account_retrieve_update_view"
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PersonalAccountSerializer

    def get_object(self):
        user_id = self.request.user.id
        user = get_object_or_404(self.queryset, id=user_id)
        return user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["username", "is_staff"]
    ordering = ["id"]
