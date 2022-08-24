from django.db import models

# Create your models here.

class Campaign(models.Model):
    event_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=50)
    contact = models.PositiveIntegerField(default=0)
