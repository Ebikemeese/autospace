from django.urls import path
from . import views

urlpatterns = [
    path('valets/dashboard/', views.valet_dashboard, name='valet_dashboard'),
]
