from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class ProductRBAC(TestCase):
    def setUp(self):
        U = get_user_model()
        self.staff = U.objects.create_user("staff@example.com", "pw")
        self.staff.is_staff = True
        self.staff.save()
        self.user = U.objects.create_user("user@example.com", "pw")

    def test_non_staff_cannot_access_admin_views(self):
        self.client.login(username="user@example.com", password="pw")
        resp = self.client.get(reverse("product_create"))
        self.assertIn(resp.status_code, (302, 403))
