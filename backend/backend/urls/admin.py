from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.views.generic.base import RedirectView


urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url='images/favicon.ico')),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    re_path(r"^ckeditor/", include("django_ckeditor_5.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", admin.site.urls),
]
