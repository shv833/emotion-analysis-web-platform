from django.urls import include, path


urlpatterns = [
    path("courses/", include("courses.urls")),
    path("groups/", include("groups.urls")),
    path("users/", include("users.urls")),
]
