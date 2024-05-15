from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = CKEditor5Field(blank=True, null=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = CKEditor5Field(blank=True, null=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    content = CKEditor5Field(blank=True, null=True)

    def __str__(self):
        return self.title
