from django.contrib.auth.models import User
from django.db import models


class CustomCake(models.Model):
    OCCASION_CHOICES = [
        ("birthday", "Birthday"),
        ("wedding", "Wedding"),
        ("christening", "Christening"),
        ("gender_reveal", "Gender Reveal"),
        ("other", "Other"),
    ]

    FLAVOR_CHOICES = [
        ("chocolate", "Chocolate"),
        ("vanilla", "Vanilla"),
        ("red_velvet", "Red Velvet"),
        ("carrot", "Carrot"),
    ]

    FILLING_CHOICES = [
        ("buttercream", "Buttercream"),
        ("chocolate_ganache", "Chocolate Ganache"),
        ("raspberry_jam", "Raspberry Jam"),
        ("lemon_curd", "Lemon Curd"),
        ("cream_cheese", "Cream Cheese"),
        ("other", "Other"),
    ]

    SIZE_CHOICES = [
        ("6", "6 inch"),
        ("8", "8 inch"),
        ("10", "10 inch"),
    ]

    # Make user optional so non-logged-in users can submit

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="custom_cakes",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True,
        help_text="Any specific requests, themes, or decoration notes.",
    )
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    flavor = models.CharField(
        max_length=20, choices=FLAVOR_CHOICES, verbose_name="flavour"
    )
    filling = models.CharField(max_length=32, choices=FILLING_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    inscription = models.CharField(max_length=100, blank=True)
    needed_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date you need the cake for (optional).",
    )
    image = models.ImageField(upload_to="custom_cakes/", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.name} ({self.user.username if self.user else 'guest'})"
