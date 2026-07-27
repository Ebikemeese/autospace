from django.urls import path
from . import views

app_name = 'valets'

urlpatterns = [
    path("", views.getValets, name="valets"),
]
