from django.db import models

# Create your models here.
from django.db import models
from accounts.models import FreelancerProfile

from django.utils import timezone

class FreelancerService(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - ${self.price} (by {self.freelancer.user.get_full_name()})"


# class FreelancerProfile(models.Model):
#     FREELANCING_CATEGORIES = (
#         ('design', 'Design'),
#         ('development', 'Development'),
#         ('writing', 'Writing'),
#         ('marketing', 'Marketing'),
#         ('consulting', 'Consulting'),
#         ('plumbing', 'Plumbing'),
#         ('electrical', 'Electrical'),
#         ('mechanic', 'Mechanic'),
#         ('painting', 'Painting'),
#         ('other', 'Other'),
#     )
#
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='freelancer_profile')
#     profile_picture = models.ImageField(upload_to='freelancer_profile_pics/', null=True, blank=True)
#     freelancing_category = models.CharField(max_length=50, choices=FREELANCING_CATEGORIES)
#     years_of_experience = models.PositiveIntegerField(default=0)
#     bio = models.TextField()
#     mobile_number = models.CharField(max_length=15)
#     address = models.TextField()
#     hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     portfolio_link = models.URLField(blank=True, null=True)
#     skills = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user.get_full_name()} - {self.get_freelancing_category_display()}"