from django.urls import path
from . import views

app_name = 'valets'

urlpatterns = [
    path('valets/dashboard/', views.valet_dashboard, name='valet_dashboard'),
]
