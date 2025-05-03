from django.db import models

# Create your models here.
from django.db import models
from accounts.models import BusinessProfile


class Event(models.Model):
    company = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    is_online = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.company.company_name}"