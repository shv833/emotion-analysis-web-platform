from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ADMIN = 0
    SUPERVISOR = 1
    TEACHER = 2
    STUDENT = 3
    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (SUPERVISOR, "Supervisor"),
        (TEACHER, "Teacher"),
        (STUDENT, "Student"),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    role = ArrayField(
        models.IntegerField(choices=ROLE_CHOICES, blank=True),
        default=[STUDENT],
        help_text="0-admin | 1-supervisor | 2-teacher | 3-student",
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    parent_info = CKEditor5Field(blank=True, null=True)  # Тільки для студентів
    group = models.ForeignKey("groups.Group", on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions " "granted to each of their groups."
        ),
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True,
        help_text=("Specific permissions for this user."),
        related_query_name="user",
    )

    objects = CustomUserManager()
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.username
