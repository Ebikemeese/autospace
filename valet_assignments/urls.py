from django.urls import path
from . import views

app_name = 'valet_assignments'

urlpatterns = [
    path("", views.getValetAssignments, name="valet_assignments"),
]
