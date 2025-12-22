from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .models import Worker, Position, TaskType, Task
from .forms import WorkerCreationForm, WorkerChangeForm


# -----------------------------
# Models
# -----------------------------
class PositionModelTest(TestCase):
    def test_str(self):
        pos = Position.objects.create(name="Oleksii")
        self.assertEqual(str(pos), "Oleksii")


class WorkerModelTest(TestCase):
    def test_str(self):
        worker = Worker.objects.create_user(
            username="harry",
            first_name="Harry",
            last_name="Potter",
            password="expelliarmus123"
        )
        self.assertEqual(str(worker), "harry (Harry Potter)")


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
            priority=Task.Priority.URGENT
        )
        self.assertIn("Defeat Harry", str(task))
        self.assertIn("urgent", str(task))


# -----------------------------
# Forms
# -----------------------------
class WorkerCreationFormTest(TestCase):
    def test_valid_form(self):
        form = WorkerCreationForm(data={
            "username": "hermione",
            "first_name": "Hermione",
            "last_name": "Granger",
            "email": "hermione@hogwarts.com",
            "position": None,
            "password1": "Wingardium123!",
            "password2": "Wingardium123!",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_username(self):
        form = WorkerCreationForm(data={
            "username": "ron__weasley",
            "first_name": "Ron",
            "last_name": "Weasley",
            "email": "ron@hogwarts.com",
            "password1": "Scabbers123!",
            "password2": "Scabbers123!",
        })
        self.assertFalse(form.is_valid())


class WorkerChangeFormTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username="snape", first_name="Severus", last_name="Snape", password="always123"
        )

    def test_change_form_valid(self):
        form = WorkerChangeForm(instance=self.worker, data={
            "username": "snape",
            "first_name": "Severus",
            "last_name": "Snape",
            "email": "snape@hogwarts.com",
            "position": None,
        })
        self.assertTrue(form.is_valid())


# -----------------------------
# Views: Registration & Activation
# -----------------------------
class RegisterActivateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_creates_inactive_user_and_sends_email(self):
        response = self.client.post(reverse("register"), {
            "username": "harry",
            "first_name": "Harry",
            "last_name": "Potter",
            "email": "harry@hogwarts.com",
            "password1": "Expelliarmus123!",
            "password2": "Expelliarmus123!",
        })
        self.assertRedirects(response, reverse("login"))
        user = Worker.objects.get(username="harry")
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Activate your account", mail.outbox[0].subject)

    def test_activate_valid_token(self):
        user = Worker.objects.create_user(
            username="draco", email="draco@hogwarts.com", password="slytherin123", is_active=False
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(reverse("activate-account", args=[uid, token]))
        self.assertRedirects(response, reverse("login"))
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_activate_invalid_token(self):
        user = Worker.objects.create_user(
            username="bellatrix", email="bellatrix@hogwarts.com", password="crucio123", is_active=False
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        response = self.client.get(reverse("activate-account", args=[uid, "wrongtoken"]))
        self.assertRedirects(response, reverse("register"))
        user.refresh_from_db()
        self.assertFalse(user.is_active)


# -----------------------------
# Views: Tasks
# -----------------------------
class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(username="harry", password="expelliarmus123")
        self.client.login(username="harry", password="expelliarmus123")
        self.tt = TaskType.objects.create(name="Potion")
        self.task = Task.objects.create(
            title="Brew Polyjuice",
            task_type=self.tt,
            assignee=self.worker
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


# -----------------------------
# Views: Profile & Avatar
# -----------------------------
class ProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(
            username="harry", first_name="Harry", last_name="Potter", password="expelliarmus123"
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        # Неавторизованный → редирект на login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_view_logged_in(self):
        self.client.login(username="harry", password="expelliarmus123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry")

    def test_profile_update(self):
        self.client.login(username="harry", password="expelliarmus123")
        response = self.client.post(reverse("profile-edit"), {
            "username": "harry",
            "first_name": "Harry",
            "last_name": "Potter",
            "email": "harry@hogwarts.com",
            "position": "",
        })
        self.assertRedirects(response, reverse("profile"))
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.email, "harry@hogwarts.com")


class AvatarChangeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(
            username="voldemort", first_name="Tom", last_name="Riddle", password="horcrux123"
        )
        self.client.login(username="voldemort", password="horcrux123")

    def test_avatar_change(self):
        response = self.client.post(reverse("avatar-change"), {"avatar": "avatar5.svg"})
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.avatar, "avatar5.svg")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "avatar5.svg")


# -----------------------------
# Views: Search & Autocomplete
# -----------------------------
class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(
            username="hermione", first_name="Hermione", last_name="Granger", password="leviosa123"
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
            username="ron", first_name="Ron", last_name="Weasley", password="scabbers123"
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
