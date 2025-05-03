from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_update, name='service_update'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
]