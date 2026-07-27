from django.urls import path
from . import views

app_name = 'garages'

urlpatterns = [
    path("", views.getGarages, name="garages"),
]
