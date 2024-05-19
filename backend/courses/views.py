from .models import Course, Module, Lesson, Task
from .serializers import TaskSerializer, CourseSerializer, LessonSerializer, ModuleSerializer
from django.db.models import Q
from common.viewsets import BaseFilteredViewSet


class CourseViewSet(BaseFilteredViewSet):
    serializer_class = CourseSerializer
    model = Course

    def teacher_filter(self, user):
        return Q(groups__teacher=user)

    def supervisor_filter(self, user):
        return Q(groups__supervisor=user)

    def student_filter(self, user):
        return Q(groups__students__student=user)


class ModuleViewSet(BaseFilteredViewSet):
    serializer_class = ModuleSerializer
    model = Module

    def teacher_filter(self, user):
        return Q(course__groups__teacher=user)

    def supervisor_filter(self, user):
        return Q(course__groups__supervisor=user)

    def student_filter(self, user):
        return Q(course__groups__students__student=user)


class LessonViewSet(BaseFilteredViewSet):
    serializer_class = LessonSerializer
    model = Lesson

    def teacher_filter(self, user):
        return Q(module__course__groups__teacher=user)

    def supervisor_filter(self, user):
        return Q(module__course__groups__supervisor=user)

    def student_filter(self, user):
        return Q(module__course__groups__students__student=user)


class TaskViewSet(BaseFilteredViewSet):
    serializer_class = TaskSerializer
    model = Task

    def teacher_filter(self, user):
        return Q(lesson__module__course__groups__teacher=user)

    def supervisor_filter(self, user):
        return Q(lesson__module__course__groups__supervisor=user)

    def student_filter(self, user):
        return Q(lesson__module__course__groups__students__student=user)
