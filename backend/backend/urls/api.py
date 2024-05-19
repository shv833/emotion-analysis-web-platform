from django.urls import path, include


v1 = "api/v1/"

urlpatterns = [
    path(v1 + "courses/", include("courses.urls")),
    path(v1 + "groups/", include("groups.urls")),
    path(v1 + "users/", include("users.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
