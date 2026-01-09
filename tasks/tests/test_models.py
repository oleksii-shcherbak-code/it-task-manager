from django.test import TestCase
from tasks.models import TaskType, Task, Worker


class TaskTypeModelTest(TestCase):
    def test_str(self):
        tt = TaskType.objects.create(name="Dark Arts")
        self.assertEqual(str(tt), "Dark Arts")


class TaskModelTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username="voldemort", password="horcrux123"
        )
        self.tt = TaskType.objects.create(name="Curse")

    def test_str(self):
        task = Task.objects.create(
            title="Defeat Harry",
            task_type=self.tt,
            assignee=self.worker,
            priority=Task.Priority.URGENT,
        )
        self.assertIn("Defeat Harry", str(task))
        self.assertIn("urgent", str(task))
