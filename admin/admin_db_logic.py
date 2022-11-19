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
        db_users = models.User.objects.all()
    except exceptions.ObjectDoesNotExist:
        return False

    users = []
    for user in db_users:
        users.append(to_dict(user))

    return users
