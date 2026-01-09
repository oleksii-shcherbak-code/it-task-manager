from django.test import TestCase
from accounts.forms import WorkerCreationForm, WorkerChangeForm
from tasks.models import Worker


class WorkerCreationFormTest(TestCase):
    def test_valid_form(self):
        form = WorkerCreationForm(
            data={
                "username": "hermione",
                "first_name": "Hermione",
                "last_name": "Granger",
                "email": "hermione@hogwarts.com",
                "position": None,
                "password1": "Wingardium123!",
                "password2": "Wingardium123!",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_username(self):
        form = WorkerCreationForm(
            data={
                "username": "ron__weasley",
                "first_name": "Ron",
                "last_name": "Weasley",
                "email": "ron@hogwarts.com",
                "password1": "Scabbers123!",
                "password2": "Scabbers123!",
            }
        )
        self.assertFalse(form.is_valid())


class WorkerChangeFormTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username="snape",
            first_name="Severus",
            last_name="Snape",
            password="always123",
        )

    def test_change_form_valid(self):
        form = WorkerChangeForm(
            instance=self.worker,
            data={
                "username": "snape",
                "first_name": "Severus",
                "last_name": "Snape",
                "email": "snape@hogwarts.com",
                "position": None,
            },
        )
        self.assertTrue(form.is_valid())
