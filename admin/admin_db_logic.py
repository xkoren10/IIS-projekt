from index import models
from index.db_logic import to_dict
import django.contrib.auth.hashers as hasher
import django.core.exceptions as exceptions


def admin_password_check(login: str, password: str):
    try:
        admin = models.Admin.objects.get(login=login)
    except exceptions.ObjectDoesNotExist:
        return False

    check = hasher.check_password(password, admin.password)

    if check:
        return admin
    else:
        return False


def admin_create(login: str, password: str):
    try:
        exists = models.Admin.objects.get(login=login)
    except exceptions.ObjectDoesNotExist:
        psw_hash = hasher.make_password(password)
        admin = models.Admin.objects.create(login=login, password=psw_hash)
        return admin

    if exists:
        return False


def get_all_users(filters=None):
    try:
        db_users = models.User.objects.all().order_by("id")
    except exceptions.ObjectDoesNotExist:
        return False

    users = []
    for user in db_users:
        users.append(to_dict(user))

    return users


def toggle_mod(user_id, promote=True):
    try:
        if promote:
            models.User.objects.filter(id=user_id).update(mod=True)
        else:
            models.User.objects.filter(id=user_id).update(mod=False)
    except exceptions.ObjectDoesNotExist:
        return False


def get_all_crops(filters=None):
    try:
        db_crops = models.Crop.objects.all().order_by("id")
    except exceptions.ObjectDoesNotExist:
        return False

    crops = []
    for crop in db_crops:
        crops.append(to_dict(crop))

    return crops


def get_all_orders(filters=None):
    try:
        db_orders = models.Order.objects.all().order_by("id")
    except exceptions.ObjectDoesNotExist:
        return False

    orders = []
    for order in db_orders:
        orders.append(to_dict(order))

    return orders


def get_all_reviews(filters=None):
    try:
        db_reviews = models.Review.objects.all().order_by("id")
    except exceptions.ObjectDoesNotExist:
        return False

    reviews = []
    for review in db_reviews:
        reviews.append(to_dict(review))

    return reviews
