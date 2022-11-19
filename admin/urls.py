from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("", views.admin_index, name="index"),
    path("login/", views.admin_login, name="login"),
    path("users/", views.admin_users_view, name="users"),
    path("crops/", views.admin_crops_view, name="crops"),
    path("harvests/", views.admin_harvests_view, name="harvests"),
    path("categories/", views.admin_categories_view, name="categories"),
    path("reviews/", views.admin_reviews_view, name="reviews"),
    path("orders/", views.admin_orders_view, name="orders"),
    path("admins/", views.admin_admins_view, name="admins"),
]
