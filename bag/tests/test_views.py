from django.test import TestCase
from django.urls import reverse
from products.models import Product
from decimal import Decimal


class BagFlowTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Cake", price=Decimal("9.99")
        )

    def test_view_bag_renders(self):
        resp = self.client.get(reverse("view_bag"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "bag/bag.html")

    def test_add_adjust_remove(self):
        self.client.post(
            reverse("add_to_bag", args=[self.product.id]),
            {"quantity": 2, "redirect_url": reverse("view_bag")},
        )
        self.assertEqual(self.client.session["bag"][str(self.product.id)], 2)
        self.client.post(
            reverse("adjust_bag", args=[self.product.id]), {"quantity": 1}
        )
        self.assertEqual(self.client.session["bag"][str(self.product.id)], 1)
        self.client.post(reverse("remove_from_bag", args=[self.product.id]))
        self.assertNotIn(
            str(self.product.id), self.client.session.get("bag", {})
        )
