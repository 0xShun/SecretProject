from datetime import date
from django.db import models


class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        today = date.today()
        year = today.year - self.birthdate.year
        cmp = ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return year - cmp

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"


class UserCredential(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.email}"
