from django.urls import path
from . import views

urlpatterns = [
    path('managers/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('valets/manage/', views.manage_valets, name='manage_valets'),
]
