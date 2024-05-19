from rest_framework import viewsets
from users.permissions import HasAccessToCourse, HasAccessToGroup
from rest_framework.permissions import IsAuthenticated
from users.models import User
from rest_framework.exceptions import PermissionDenied


class BaseFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & (HasAccessToCourse | HasAccessToGroup)]

    def get_queryset(self):
        user = self.request.user
        queryset = self.model.objects.none()

        if User.TEACHER in user.role:
            queryset = self.model.objects.filter(self.teacher_filter(user))
        elif User.SUPERVISOR in user.role:
            queryset = self.model.objects.filter(self.supervisor_filter(user))
        elif User.STUDENT in user.role:
            queryset = self.model.objects.filter(self.student_filter(user))
        elif user.is_superuser or User.ADMIN in user.role:
            queryset = self.model.objects.all()

        return queryset

    def teacher_filter(self, user):
        raise NotImplementedError("You must define teacher_filter method")

    def supervisor_filter(self, user):
        raise NotImplementedError("You must define supervisor_filter method")

    def student_filter(self, user):
        raise NotImplementedError("You must define student_filter method")

    def create(self, request, *args, **kwargs):
        user = request.user
        if User.TEACHER in user.role or User.STUDENT in user.role:
            raise PermissionDenied("You do not have permission to create this object.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if User.TEACHER in user.role or User.STUDENT in user.role:
            raise PermissionDenied("You do not have permission to update this object.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        if User.TEACHER in user.role or User.STUDENT in user.role:
            raise PermissionDenied("You do not have permission to update this object.")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if User.TEACHER in user.role or User.STUDENT in user.role:
            raise PermissionDenied("You do not have permission to delete this object.")
        return super().destroy(request, *args, **kwargs)
