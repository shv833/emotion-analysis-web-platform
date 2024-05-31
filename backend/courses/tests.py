from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from groups.models import Group
from courses.models import Course, Module, Lesson, Task


class CourseViewSetTestCase(TestCase):
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

        self.url = reverse("course-list")

    def test_list_courses_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.course.id)

    def test_list_courses_as_supervisor(self):
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.course.id)

    def test_list_courses_as_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_course_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.url, {"title": "New Course"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, {"title": "New Course"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(
            reverse("course-detail", args=[self.course.id]), {"title": "Updated Course"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("course-detail", args=[self.course.id]), {"title": "Updated Course"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Course")

    def test_delete_course_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(reverse("course-detail", args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("course-detail", args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class ModuleViewSetTestCase(TestCase):
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
        self.module = Module.objects.create(course=self.course, title="Test Module")
        self.group = Group.objects.create(
            title="Test Group", course=self.course, teacher=self.teacher, supervisor=self.supervisor
        )

        self.url = reverse("module-list")

    def test_list_modules_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.module.id)

    def test_list_modules_as_supervisor(self):
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.module.id)

    def test_list_modules_as_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_module_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.url, {"course": self.course.id, "title": "New Module"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_module_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, {"course": self.course.id, "title": "New Module"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 2)

    def test_update_module_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(
            reverse("module-detail", args=[self.module.id]), {"title": "Updated Module"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_module_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("module-detail", args=[self.module.id]), {"title": "Updated Module"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.module.refresh_from_db()
        self.assertEqual(self.module.title, "Updated Module")

    def test_delete_module_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(reverse("module-detail", args=[self.module.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_module_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("module-detail", args=[self.module.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.count(), 0)


class LessonViewSetTestCase(TestCase):
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
        self.module = Module.objects.create(course=self.course, title="Test Module")
        self.lesson = Lesson.objects.create(module=self.module, title="Test Lesson")
        self.group = Group.objects.create(
            title="Test Group", course=self.course, teacher=self.teacher, supervisor=self.supervisor
        )

        self.url = reverse("lesson-list")

    def test_list_lessons_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.lesson.id)

    def test_list_lessons_as_supervisor(self):
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.lesson.id)

    def test_list_lessons_as_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_lesson_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.url, {"module": self.module.id, "title": "New Lesson"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, {"module": self.module.id, "title": "New Lesson"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(
            reverse("lesson-detail", args=[self.lesson.id]), {"title": "Updated Lesson"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("lesson-detail", args=[self.lesson.id]), {"title": "Updated Lesson"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(reverse("lesson-detail", args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("lesson-detail", args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class TaskViewSetTestCase(TestCase):
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
        self.module = Module.objects.create(course=self.course, title="Test Module")
        self.lesson = Lesson.objects.create(module=self.module, title="Test Lesson")
        self.task = Task.objects.create(lesson=self.lesson, title="Test Task", type="example", content="Test Content")
        self.group = Group.objects.create(
            title="Test Group", course=self.course, teacher=self.teacher, supervisor=self.supervisor
        )

        self.url = reverse("task-list")

    def test_list_tasks_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.task.id)

    def test_list_tasks_as_supervisor(self):
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.task.id)

    def test_list_tasks_as_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_task_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(
            self.url,
            {"lesson": self.lesson.id, "title": "New Task", "type": "example", "content": "New Content"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            self.url,
            {"lesson": self.lesson.id, "title": "New Task", "type": "example", "content": "New Content"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(
            reverse("task-detail", args=[self.task.id]), {"title": "Updated Task"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("task-detail", args=[self.task.id]), {"title": "Updated Task"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_delete_task_as_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(reverse("task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
