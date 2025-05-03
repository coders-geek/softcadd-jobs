from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, JobSeekerProfile, BusinessProfile, FreelancerProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class JobSeekerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'job_seeker'
        if commit:
            user.save()
        return user


class BusinessRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=200)
    company_type = forms.ChoiceField(choices=BusinessProfile.COMPANY_TYPE_CHOICES)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'company_name', 'company_type', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'business'
        if commit:
            user.save()
        return user


class FreelancerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    freelancing_category = forms.ChoiceField(choices=FreelancerProfile.FREELANCING_CATEGORIES)
    years_of_experience = forms.IntegerField(min_value=0)

    class Meta:
        model = CustomUser
        fields = (
        'username', 'email', 'first_name', 'last_name', 'freelancing_category', 'years_of_experience', 'password1',
        'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'freelancer'
        if commit:
            user.save()
            FreelancerProfile.objects.create(
                user=user,
                freelancing_category=self.cleaned_data['freelancing_category'],
                years_of_experience=self.cleaned_data['years_of_experience']
            )
        return user

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'freelancer'
        if commit:
            user.save()
            FreelancerProfile.objects.create(
                user=user,
                freelancing_category=self.cleaned_data['freelancing_category'],
                years_of_experience=self.cleaned_data['years_of_experience']
            )
        return user


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        exclude = ('user',)
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        exclude = ('user', 'is_approved')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'services_products': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            'profile_picture',
            'freelancing_category',
            'years_of_experience',
            'bio',
            'mobile_number',
            'address',
            'hourly_rate',
            'portfolio_link',
            'skills'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3}),
        }