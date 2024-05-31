from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from groups.models import Group, GroupStudent
from courses.models import Course


class GroupViewSetTestCase(TestCase):
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
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123", role=[User.ADMIN]
        )

        self.course = Course.objects.create(title="Test Course")
        self.group = Group.objects.create(
            title="Test Group", course=self.course, teacher=self.teacher, supervisor=self.supervisor
        )

        self.url = reverse("group-list")

    def test_list_groups_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.group.id)

    def test_list_groups_as_supervisor(self):
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.group.id)

    def test_list_groups_as_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_group_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(
            self.url,
            {
                "title": "New Group",
                "course": self.course.id,
                "teacher": self.teacher.id,
                "supervisor": self.supervisor.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_create_group_as_admin(self):
    #     self.client.force_authenticate(user=self.admin)
    #     response = self.client.post(self.url, {"title": "New Group", "course": self.course.id, "teacher": self.teacher.id, "supervisor": self.supervisor.id}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 2)

    def test_update_group_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(
            reverse("group-detail", args=[self.group.id]), {"title": "Updated Group"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_group_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("group-detail", args=[self.group.id]), {"title": "Updated Group"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group.refresh_from_db()
        self.assertEqual(self.group.title, "Updated Group")

    def test_delete_group_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(reverse("group-detail", args=[self.group.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_group_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("group-detail", args=[self.group.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Group.objects.count(), 0)


class GroupStudentViewSetTestCase(TestCase):
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
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123", role=[User.ADMIN]
        )

        self.course = Course.objects.create(title="Test Course")
        self.group = Group.objects.create(
            title="Test Group", course=self.course, teacher=self.teacher, supervisor=self.supervisor
        )
        self.group_student = GroupStudent.objects.create(group=self.group, student=self.student)

        self.url = reverse("groupstudent-list")

    def test_list_group_students_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.group_student.id)

    def test_list_group_students_as_supervisor(self):
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.group_student.id)

    def test_list_group_students_as_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_group_student_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.url, {"group": self.group.id, "student": self.student.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_create_group_student_as_admin(self):
    #     self.client.force_authenticate(user=self.admin)
    #     response = self.client.post(self.url, {"group": self.group.id, "student": self.student.id}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(GroupStudent.objects.count(), 2)

    def test_update_group_student_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(
            reverse("groupstudent-detail", args=[self.group_student.id]), {"is_active": False}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_group_student_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("groupstudent-detail", args=[self.group_student.id]), {"is_active": False}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group_student.refresh_from_db()
        self.assertFalse(self.group_student.is_active)

    def test_delete_group_student_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(reverse("groupstudent-detail", args=[self.group_student.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_group_student_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("groupstudent-detail", args=[self.group_student.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GroupStudent.objects.count(), 0)
