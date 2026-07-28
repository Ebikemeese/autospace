from django.urls import path
from . import views

app_name = 'verification'

urlpatterns = [
    path('verification/toggle/<int:garage_id>/', views.toggle_verification, name='toggle_verification'),
]
