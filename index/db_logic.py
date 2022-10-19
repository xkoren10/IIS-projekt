from django.db import connection
import django.contrib.auth.hashers as hasher


def user_get_by_id(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_name, email FROM users WHERE id=%s" % str(user_id))
        row = cursor.fetchone()
    return row


def user_create(username: str, password: str, email=None):
    psw_hash = hasher.make_password(password)
    with connection.cursor() as cursor:
        if email:
            cursor.execute("INSERT INTO users VALUES (DEFAULT, '%s', '%s', '%s')" % (str(username), str(email), str(psw_hash)))
        else:
            cursor.execute("INSERT INTO users VALUES (DEFAULT, '%s', NULL, '%s')" % (str(username), str(psw_hash)))
    return True


def password_check(username: str, password: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT password FROM users WHERE user_name='%s'" % username)
        row = cursor.fetchone()
        if not row:
            return False
    return hasher.check_password(password, row[0])
