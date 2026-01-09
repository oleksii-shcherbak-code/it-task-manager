from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import Worker, TaskType, Task


class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(
            username="harry", password="expelliarmus123"
        )
        self.client.login(username="harry", password="expelliarmus123")
        self.tt = TaskType.objects.create(name="Potion")
        self.task = Task.objects.create(
            title="Brew Polyjuice", task_type=self.tt, assignee=self.worker
        )

    def test_task_list_view(self):
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brew Polyjuice")

    def test_toggle_task_status(self):
        self.assertFalse(self.task.is_completed)
        response = self.client.post(reverse("task-toggle", args=[self.task.pk]))
        self.assertRedirects(response, reverse("task-detail", args=[self.task.pk]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
