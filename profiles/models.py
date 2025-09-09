from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    default_phone_number = models.CharField(max_length=32, blank=True)
    default_country = models.CharField(max_length=40, blank=True)
    default_postcode = models.CharField(max_length=20, blank=True)
    default_town_or_city = models.CharField(max_length=40, blank=True)
    default_street_address1 = models.CharField(max_length=80, blank=True)
    default_street_address2 = models.CharField(max_length=80, blank=True)
    def __str__(self):
        return f"{self.user.username}"
