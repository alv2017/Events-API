from django.urls import path

from .views import (
    PersonalAccountCreateView,
    PersonalAccountRetrieveUpdateView,
    UserViewSet,
)

urlpatterns = [
    path(
        "account/",
        PersonalAccountCreateView.as_view(),
        name=PersonalAccountCreateView.name,
    ),
    path(
        "account/me/",
        PersonalAccountRetrieveUpdateView.as_view(),
        name=PersonalAccountRetrieveUpdateView.name,
    ),
    path(
        "manage/",
        UserViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="user_list_create_view",
    ),
    path(
        "manage/<int:pk>/",
        UserViewSet.as_view(
            {"get": "retrieve", "put": "partial_update", "delete": "destroy"}
        ),
        name="user_retrieve_update_delete_view",
    ),
]
