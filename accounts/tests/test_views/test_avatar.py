from django.test import TestCase, Client
from django.urls import reverse
from tasks.models import Worker


class AvatarChangeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create_user(
            username="voldemort",
            first_name="Tom",
            last_name="Riddle",
            password="horcrux123",
        )
        self.client.login(username="voldemort", password="horcrux123")

    def test_avatar_change(self):
        response = self.client.post(reverse("avatar-change"), {"avatar": "avatar5.svg"})
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.avatar, "avatar5.svg")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "avatar5.svg")
