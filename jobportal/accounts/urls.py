from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/job-seeker/', views.register_job_seeker, name='register_job_seeker'),
    path('register/business/', views.register_business, name='register_business'),
    path('register/freelancer/', views.register_freelancer, name='register_freelancer'),
    path('job-seeker/profile/', views.job_seeker_profile, name='job_seeker_profile'),
    path('business/profile/', views.business_profile, name='business_profile'),
    path('freelancer/profile/', views.freelancer_profile, name='freelancer_profile'),
]