from django.db import connection
import django.contrib.auth.hashers as hasher
from . import models


"""
WARNING:
BY USING *(ASTERISK) ON ROW/LIST YOU WILL PUT DATA INTO OBJECT IN ORDER AS IT IS IN SQL QUERY
THAT MAY CAUSE A LOT OF PROBLEMS SO MAKE SURE ORDER OF INIT FUNCTION IN MODEL IS SAME AS THE ONE IN YOUR QUERY

Also check what required arguments you need in object`s init function
"""


def user_get_by_id(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, user_name, email, is_mod FROM users WHERE id=%s" % str(user_id))
        row = cursor.fetchone()

    if not row:
        return False

    user = models.User(*row)
    return user


def user_create(username: str, password: str, email=None):
    # TODO check if user(name) already exists
    psw_hash = hasher.make_password(password)
    with connection.cursor() as cursor:
        # create user in db with or without email
        if email:
            cursor.execute("INSERT INTO users VALUES (DEFAULT, '%s', '%s', '%s')" % (str(username), str(email), str(psw_hash)))
        else:
            cursor.execute("INSERT INTO users VALUES (DEFAULT, '%s', NULL, '%s')" % (str(username), str(psw_hash)))

        # get created user from db
        cursor.execute("SELECT id, user_name, email, is_mod FROM users WHERE user_name='%s'" % str(username))
        row = cursor.fetchone()

    if not row:
        # now this would be bad
        return False

    return models.User(*row)


def password_check(username: str, password: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, password FROM users WHERE user_name='%s'" % username)
        row = cursor.fetchone()

    # check if any user was found
    if not row:
        return False

    # check hashed password
    check = hasher.check_password(password, row[1])

    if check:
        # if ok, get user
        return user_get_by_id(row[0])
    else:
        return False


def get_top_crops():
    with connection.cursor() as cursor:
        # note: deleted stars from SELECT
        cursor.execute("SELECT crops.id, crop_name, category, price FROM crops JOIN reviews on crops.id = reviews.reviewed_crop order by stars desc limit 5;")
        rows = cursor.fetchall()

    if not rows:
        return False

    crops = []
    for row in rows:
        crops.append(models.Crop(*row))

    return crops


def get_new_crops():
    with connection.cursor() as cursor:
        # note: deleted date from SELECT
        cursor.execute("SELECT crops.id, crop_name, category, price FROM crops order by crop_year desc limit 5;")
        rows = cursor.fetchall()

    if not rows:
        return False

    crops = []
    for row in rows:
        crops.append(models.Crop(*row))

    return crops
