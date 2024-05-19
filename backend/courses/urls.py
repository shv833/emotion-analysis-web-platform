from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, LessonViewSet, TaskViewSet

# Create a router and register the viewsets with a basename
router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"modules", ModuleViewSet, basename="module")
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"tasks", TaskViewSet, basename="task")

# Include the router URLs in the urlpatterns
urlpatterns = [
    path("", include(router.urls)),
]
