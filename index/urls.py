from django.urls import path
from . import views

app_name = "index"
# URL patterns for 'index' app
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("offers/", views.offers, name="offers"),
    path("harvests/", views.harvests, name="harvests"),
    path("product_detail/<int:product_id>/", views.product_detail, name="product_detail"),
    path("harvest_detail/<int:harvest_id>/", views.harvest_detail, name="harvest_detail")
]
# path(URL, VIEW, NAME)
# URL is string with URL address AND '/' on its end
# VIEW is function / object with backend implementation from views.py
# NAME is string name of URL
