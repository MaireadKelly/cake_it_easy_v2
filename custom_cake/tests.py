from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import CustomCake


class CustomCakeViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="pass"
        )
        self.client.login(username="tester", password="pass")
        self.valid_data = {
            "name": "Test Cake",
            "occasion": "birthday",
            "flavor": "chocolate",
            "size": "6",
            "inscription": "Happy",
            "description": "desc",
        }

    def test_create_custom_cake(self):
        response = self.client.post(
            reverse("create_custom_cake"),
            self.valid_data,
            follow=True,
        )
        self.assertEqual(CustomCake.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("created successfully" in m.message for m in messages),
            "Success message not found after creation.",
        )

    def test_update_custom_cake(self):
        cake = CustomCake.objects.create(user=self.user, **self.valid_data)
        update_data = self.valid_data.copy()
        update_data["name"] = "Updated Cake"

        response = self.client.post(
            reverse("update_custom_cake", args=[cake.pk]),
            update_data,
            follow=True,
        )
        cake.refresh_from_db()
        self.assertEqual(cake.name, "Updated Cake")
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("updated successfully" in m.message for m in messages),
            "Success message not found after update.",
        )

    def test_delete_custom_cake(self):
        cake = CustomCake.objects.create(user=self.user, **self.valid_data)

        response = self.client.post(
            reverse("delete_custom_cake", args=[cake.pk]),
            follow=True,
        )
        self.assertFalse(
            CustomCake.objects.filter(pk=cake.pk).exists(),
            "Cake was not deleted from the database.",
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("deleted successfully" in m.message for m in messages),
            "Success message not found after deletion.",
        )

    def test_create_invalid_shows_error_message(self):
        invalid = self.valid_data.copy()
        invalid["name"] = ""  # name is required

        response = self.client.post(
            reverse("create_custom_cake"),
            invalid,
            follow=True,
        )
        self.assertEqual(CustomCake.objects.count(), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Error creating custom cake" in m.message for m in messages),
            "Expected error message not found after invalid form submission.",
        )
