from django.db import models
from users.models import User
from courses.models import Course
from django.db.models import Q
from django_ckeditor_5.fields import CKEditor5Field


class Group(models.Model):
    title = models.CharField(max_length=255)
    date_started = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, related_name="groups", on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        User,
        related_name="teaching_groups",
        on_delete=models.CASCADE,
        limit_choices_to={"role__contains": [User.TEACHER]},
    )
    supervisor = models.ForeignKey(
        User,
        related_name="supervising_groups",
        on_delete=models.CASCADE,
        limit_choices_to=Q(role__contains=[User.SUPERVISOR]) | Q(role__contains=[User.ADMIN]),
    )
    description = CKEditor5Field(blank=True, null=True)

    def __str__(self):
        return self.title


class GroupStudent(models.Model):
    group = models.ForeignKey(Group, related_name="students", on_delete=models.CASCADE)
    student = models.ForeignKey(
        User,
        related_name="student_groups",
        on_delete=models.CASCADE,
        limit_choices_to={"role__contains": [User.STUDENT]},
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.username} in group {self.group.id}"
