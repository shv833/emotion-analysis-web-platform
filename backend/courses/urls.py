from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, LessonViewSet, TaskViewSet


router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"modules", ModuleViewSet, basename="module")
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
]
