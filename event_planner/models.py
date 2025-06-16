from django.db import models
from accounts.models import UserProfile

# Create your models here.
class Event(models.Model):

    location = models.OneToOneField('EventLocation', on_delete=models.CASCADE, unique=True)
    event_name = models.CharField(max_length=255)
    event_description = models.CharField(max_length=255)
    event_keywords = models.TextField()
    event_organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # links to user_profile.id
    event_date = models.DateTimeField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.event_name


class EventAddress(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street_address}, {self.barangay}, {self.city}"


class EventLocation(models.Model):
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return f"{self.lat}, {self.long}"