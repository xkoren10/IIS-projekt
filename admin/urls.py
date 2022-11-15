from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("", views.index, name="index"),
    path("admin_login/", views.index, name="index"),
]
