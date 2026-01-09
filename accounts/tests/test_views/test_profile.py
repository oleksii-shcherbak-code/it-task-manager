from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import Worker


class ProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(
            username="harry",
            first_name="Harry",
            last_name="Potter",
            password="expelliarmus123",
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_view_logged_in(self):
        self.client.login(username="harry", password="expelliarmus123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry")

    def test_profile_update(self):
        self.client.login(username="harry", password="expelliarmus123")
        response = self.client.post(
            reverse("profile_edit"),
            {
                "username": "harry",
                "first_name": "Harry",
                "last_name": "Potter",
                "email": "harry@hogwarts.com",
                "position": "",
            },
        )
        self.assertRedirects(response, reverse("profile"))
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.email, "harry@hogwarts.com")
