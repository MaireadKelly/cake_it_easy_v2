from django.db import models
from django.contrib.auth.models import User

class CustomCake(models.Model):
    OCCASION_CHOICES = [
        ('birthday', 'Birthday'),
        ('wedding', 'Wedding'),
        ('christening', 'Christening'),
        ('gender_reveal', 'Gender Reveal'),
        ('other', 'Other'),
    ]

    FLAVOR_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('vanilla', 'Vanilla'),
        ('red_velvet', 'Red Velvet'),
        ('carrot', 'Carrot'),
    ]

    SIZE_CHOICES = [
        ('6', '6 inch'),
        ('8', '8 inch'),
        ('10', '10 inch'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_cakes')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text="Any specific requests, themes, or decoration notes.")
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    flavor = models.CharField(max_length=20, choices=FLAVOR_CHOICES, verbose_name='Flavour')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    inscription = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='custom_cakes/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.user.username})'
