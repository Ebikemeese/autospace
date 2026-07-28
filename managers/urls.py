from django.urls import path
from . import views

app_name = 'managers'

urlpatterns = [
    path('managers/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('valets/manage/', views.manage_valets, name='manage_valets'),
]
