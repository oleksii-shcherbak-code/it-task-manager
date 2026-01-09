from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from tasks.models import Worker


class RegisterActivateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_creates_inactive_user_and_sends_email(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "harry",
                "first_name": "Harry",
                "last_name": "Potter",
                "email": "harry@hogwarts.com",
                "password1": "Expelliarmus123!",
                "password2": "Expelliarmus123!",
            },
        )
        self.assertRedirects(response, reverse("login"))
        user = Worker.objects.get(username="harry")
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Activate your account", mail.outbox[0].subject)

    def test_activate_valid_token(self):
        user = Worker.objects.create_user(
            username="draco",
            email="draco@hogwarts.com",
            password="slytherin123",
            is_active=False,
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(reverse("activate-account", args=[uid, token]))
        self.assertRedirects(response, reverse("login"))
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_activate_invalid_token(self):
        user = Worker.objects.create_user(
            username="bellatrix",
            email="bellatrix@hogwarts.com",
            password="crucio123",
            is_active=False,
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        response = self.client.get(reverse("activate-account", args=[uid, "wrongtoken"]))
        self.assertRedirects(response, reverse("register"))
        user.refresh_from_db()
        self.assertFalse(user.is_active)
