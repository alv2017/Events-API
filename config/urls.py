from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Auth
    path("api/v1/auth/", include("auth.urls")),
    # User
    path("api/v1/user/", include("user.urls")),
    # Events
    path("api/v1/event/", include("event.urls")),
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += [
        # Django Debug Toolbar
        path("__debug__/", include("debug_toolbar.urls")),

        # DRF Spectacular API Schema and Swagger Docs
        path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]



