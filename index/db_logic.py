from django.db import connection
import django.contrib.auth.hashers as hasher
from . import models
import django.core.exceptions as exceptions


"""
WARNING:
BY USING *(ASTERISK) ON ROW/LIST YOU WILL PUT DATA INTO OBJECT IN ORDER AS IT IS IN SQL QUERY
THAT MAY CAUSE A LOT OF PROBLEMS SO MAKE SURE ORDER OF INIT FUNCTION IN MODEL IS SAME AS THE ONE IN YOUR QUERY

Also check what required arguments you need in object`s init function

punishment is death
"""


def user_get_by_id(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, user_name, email, is_mod FROM users WHERE id=%s" % str(user_id))
        row = cursor.fetchone()

    if not row:
        return False

    user = models.User(*row)
    return user


def user_create(username: str, password: str, email=''):
    # TODO check if user(name) already exists
    user_exists = models.User.objects.get(user_name=username)

    if user_exists:
        return False

    psw_hash = hasher.make_password(password)

    user = models.User.objects.create(user_name=username, email=email, password=psw_hash, mod=False)

    if not user:
        # now this would be bad
        return False

    return user


def password_check(username: str, password: str):
    # check if any user was found
    try:
        user = models.User.objects.get(user_name=username)

    except exceptions.ObjectDoesNotExist:
        return False

    # check hashed password
    check = hasher.check_password(password, user.password)

    if check:
        # if ok, get user
        return user
    else:
        return False


def get_top_crops():

    return False



def get_new_crops():

    return False


