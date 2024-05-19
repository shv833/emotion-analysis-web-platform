from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, GroupStudentViewSet

router = DefaultRouter()
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"groupstudents", GroupStudentViewSet, basename="groupstudent")

urlpatterns = [
    path("", include(router.urls)),
]
