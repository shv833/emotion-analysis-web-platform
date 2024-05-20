from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


v1 = "api/v1/"

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url="images/favicon.ico")),

    path(v1 + "auth/", include("djoser.urls")),
    re_path(v1 + r"^auth/", include("djoser.urls.jwt")),

    path(v1 + "courses/", include("courses.urls")),
    path(v1 + "groups/", include("groups.urls")),
    path(v1 + "users/", include("users.urls")),

    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    re_path(r"^ckeditor/", include("django_ckeditor_5.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
