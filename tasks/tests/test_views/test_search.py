from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import Worker, TaskType, Task


class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(
            username="hermione",
            first_name="Hermione",
            last_name="Granger",
            password="leviosa123",
        )
        self.task_type = TaskType.objects.create(name="Magic")
        self.task = Task.objects.create(
            title="Learn Levitation",
            assignee=self.worker,
            task_type=self.task_type,
        )
        self.client.login(username="hermione", password="leviosa123")

    def test_search_empty_query(self):
        response = self.client.get(reverse("search"), {"q": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["workers"], [])
        self.assertEqual(response.context["tasks"], [])

    def test_search_worker_found(self):
        response = self.client.get(reverse("search"), {"q": "Hermione"})
        self.assertContains(response, "Hermione")

    def test_search_task_found(self):
        response = self.client.get(reverse("search"), {"q": "Levitation"})
        self.assertContains(response, "Learn Levitation")


class SearchSuggestTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(
            username="ron",
            first_name="Ron",
            last_name="Weasley",
            password="scabbers123",
        )
        self.task_type = TaskType.objects.create(name="Magic")
        self.task = Task.objects.create(
            title="Defeat Troll",
            assignee=self.worker,
            task_type=self.task_type,
        )

    def test_suggest_requires_auth(self):
        response = self.client.get(reverse("search-suggest"), {"q": "Ron"})
        self.assertJSONEqual(response.content, [])

    def test_suggest_worker(self):
        self.client.login(username="ron", password="scabbers123")
        response = self.client.get(reverse("search-suggest"), {"q": "Ron"})
        data = response.json()
        self.assertEqual(data[0]["type"], "worker")
        self.assertEqual(data[0]["name"], "Ron Weasley")

    def test_suggest_task(self):
        self.client.login(username="ron", password="scabbers123")
        response = self.client.get(reverse("search-suggest"), {"q": "Troll"})
        data = response.json()
        self.assertEqual(data[0]["type"], "task")
        self.assertEqual(data[0]["name"], "Defeat Troll")
