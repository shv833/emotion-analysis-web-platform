from django.contrib import admin
from .models import Course, Module, Lesson, Task


admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Task)
