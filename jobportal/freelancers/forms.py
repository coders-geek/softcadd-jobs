from django import forms
from .models import FreelancerService

class FreelancerServiceForm(forms.ModelForm):
    class Meta:
        model = FreelancerService
        fields = ['title', 'description', 'price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }