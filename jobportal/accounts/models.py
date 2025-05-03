from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('business', 'Business/Vendor'),
        ('freelancer', 'Professional/Freelancer'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_approved = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='job_seeker_profile')
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    current_ctc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_ctc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    languages = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user.get_full_name()} - Job Seeker"


class BusinessProfile(models.Model):
    COMPANY_TYPE_CHOICES = (
        ('business', 'Business'),
        ('vendor', 'Vendor'),
        ('startup', 'Startup'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='business_profile')
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    description = models.TextField()
    services_products = models.TextField()
    registration_document = models.FileField(
        upload_to='business_docs/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        help_text="Upload company registration document for verification"
    )
    address = models.TextField()
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name

from django.utils import timezone

class FreelancerProfile(models.Model):
    FREELANCING_CATEGORIES = (
        ('design', 'Design'),
        ('development', 'Development'),
        ('writing', 'Writing'),
        ('marketing', 'Marketing'),
        ('consulting', 'Consulting'),
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('mechanic', 'Mechanic'),
        ('painting', 'Painting'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='freelancer_profile')
    profile_picture = models.ImageField(upload_to='freelancer_profile_pics/', null=True, blank=True)
    freelancing_category = models.CharField(max_length=50, choices=FREELANCING_CATEGORIES,default='other')
    years_of_experience = models.PositiveIntegerField(default=0)
    bio = models.TextField()
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    portfolio_link = models.URLField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_freelancing_category_display()}"