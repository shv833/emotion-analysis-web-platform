from .models import Group, GroupStudent
from .serializers import GroupSerializer, GroupStudentSerializer
from django.db.models import Q
from common.viewsets import BaseFilteredViewSet
from rest_framework import generics


class GroupViewSet(BaseFilteredViewSet):
    serializer_class = GroupSerializer
    model = Group

    def teacher_filter(self, user):
        return Q(teacher=user)

    def supervisor_filter(self, user):
        return Q(supervisor=user)

    def student_filter(self, user):
        return Q(students__student=user)


class GroupStudentViewSet(BaseFilteredViewSet):
    serializer_class = GroupStudentSerializer
    model = GroupStudent

    def teacher_filter(self, user):
        return Q(group__teacher=user)

    def supervisor_filter(self, user):
        return Q(group__supervisor=user)

    def student_filter(self, user):
        return Q(student=user)
