from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/apply/', views.job_application, name='job_application'),
    path('post/', views.job_post, name='job_post'),
    path('business/jobs/', views.business_job_list, name='business_job_list'),
    path('business/applications/', views.business_applications, name='business_applications'),
    path('business/applications/<int:pk>/', views.application_detail, name='application_detail'),
]