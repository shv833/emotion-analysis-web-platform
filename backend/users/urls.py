from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreate, StudentListView, LogoutView


urlpatterns = [
    path("register/", UserCreate.as_view(), name="user-register"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("students/", StudentListView.as_view(), name="student-list"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
]
