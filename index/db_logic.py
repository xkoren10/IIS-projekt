from django.db import connection
import django.contrib.auth.hashers as hasher


def user_get_by_id(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_name, email FROM users WHERE id=%s" % str(user_id))
        row = cursor.fetchone()
    return row


def user_create(username: str, password: str, email=None):
    # TODO check if user(name) already exists
    psw_hash = hasher.make_password(password)
    with connection.cursor() as cursor:
        if email:
            cursor.execute("INSERT INTO users VALUES (DEFAULT, '%s', '%s', '%s')" % (str(username), str(email), str(psw_hash)))
        else:
            cursor.execute("INSERT INTO users VALUES (DEFAULT, '%s', NULL, '%s')" % (str(username), str(psw_hash)))

        cursor.execute("SELECT id FROM users WHERE user_name='%s'" % str(username))
        row = cursor.fetchone()
    return row


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
        return row[0]
    else:
        return False


def get_top_crops():
    with connection.cursor() as cursor:
        cursor.execute("SELECT crops.id, crop_name, description, category, price, stars FROM crops JOIN reviews on crops.id = reviews.reviewed_crop order by stars desc limit 5;")
        row = cursor.fetchall()
        if not row:
            return False
    return row

def get_new_crops():
    with connection.cursor() as cursor:
        cursor.execute("SELECT crops.id, crop_name, description, category, price, crop_year FROM crops order by crop_year desc limit 5;")
        row = cursor.fetchall()
        if not row:
            return False
    return row
