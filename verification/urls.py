from django.urls import path
from . import views

app_name = 'verification'

urlpatterns = [
    path("", views.getVerification, name="verification"),
]
