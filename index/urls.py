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
    path("new_crop/<int:crop_id>/", views.new_crop, name="new_crop"),
    path("profile/", views.profile, name="profile"),
    path("category_moderation", views.moderation, name="moderation"),
    path("new_category", views.new_category, name="new_category"),
    path("new_review/<int:crop_id>", views.new_review, name="new_review"),
    path("cart/", views.cart_detail, name="cart"),
    path("product_detail/<int:product_id>/", views.product_detail, name="product_detail"),
    path("harvest_detail/<int:harvest_id>/", views.harvest_detail, name="harvest_detail"),
    path("new_harvest/<int:harvest_id>/", views.new_harvest, name="new_harvest"),
    path("blue_lobster/", views.blue_lobster, name="lobster")
]
# path(URL, VIEW, NAME)
# URL is string with URL address AND '/' on its end
# VIEW is function / object with backend implementation from views.py
# NAME is string name of URL
