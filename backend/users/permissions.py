from rest_framework.permissions import BasePermission
from .models import User
from courses.models import Course, Module, Lesson, Task
from groups.models import Group, GroupStudent


class HasAccessToCourse(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if isinstance(obj, Course):
            course = obj
        elif isinstance(obj, Module):
            course = obj.course
        elif isinstance(obj, Lesson):
            course = obj.module.course
        elif isinstance(obj, Task):
            course = obj.lesson.module.course
        else:
            return False

        if user.is_superuser or User.ADMIN in user.role:
            return True
        elif User.TEACHER in user.role and course.groups.filter(teacher=user).exists():
            return True
        elif User.STUDENT in user.role and GroupStudent.objects.filter(group__course=course, student=user).exists():
            return True
        elif User.SUPERVISOR in user.role and course.groups.filter(supervisor=user).exists():
            return True
        return False


class HasAccessToGroup(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or User.ADMIN in user.role:
            return True
        elif isinstance(obj, Group):
            group = obj
        elif isinstance(obj, GroupStudent):
            group = obj.group
        else:
            return False

        if User.TEACHER in user.role and group.teacher == user:
            return True
        elif User.SUPERVISOR in user.role and group.supervisor == user:
            return True
        elif User.STUDENT in user.role and group.students.filter(student=user).exists():
            return True
        return False
