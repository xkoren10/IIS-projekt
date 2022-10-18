from django.db import connection


def get_user_by_id(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_name, email FROM users WHERE id=%s", str(user_id))
        row = cursor.fetchone()
    return row
