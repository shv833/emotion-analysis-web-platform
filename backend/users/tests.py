from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from groups.models import Group, GroupStudent, Course
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user-register")
        self.user_data = {
            "username": "testuser",
            "phone_number": "1234567890",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "password123",
        }

    def test_create_user(self):
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_create_user_missing_fields(self):
        user_data = self.user_data.copy()
        user_data.pop("email")
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StudentListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            username="teacher", email="teacher@example.com", password="password123", role=[User.TEACHER]
        )
        self.supervisor = User.objects.create_user(
            username="supervisor", email="supervisor@example.com", password="password123", role=[User.SUPERVISOR]
        )
        self.student = User.objects.create_user(
            username="student", email="student@example.com", password="password123", role=[User.STUDENT]
        )
        self.course = Course.objects.create(title="Test Course")
        self.group = Group.objects.create(course=self.course, teacher=self.teacher, supervisor=self.supervisor)
        GroupStudent.objects.create(group=self.group, student=self.student)
        self.url = reverse("student-list")

    def test_student_list_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["student"]["id"], self.student.id)

    def test_student_list_as_supervisor(self):
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["student"]["id"], self.student.id)

    def test_student_list_as_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.url = reverse("user-logout")

    def test_logout(self):
        response = self.client.post(self.url, {"refresh": self.refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_invalid_token(self):
        response = self.client.post(self.url, {"refresh": "invalidtoken"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
