# {% load poll_extras %} v templates
from django import template
from admin import admin_db_logic as admin_db
from index import db_logic as db
register = template.Library()


@register.simple_tag()
def get_user_name(user_id):
    user_name = db.user_get_by_id(user_id)["user_name"]
    if not user_name:
        return ""
    return user_name


@register.simple_tag()
def get_crop_name(crop_id):
    crop_name = db.crop_get_by_id(crop_id)["crop_name"]
    if not crop_name:
        return ""
    return crop_name


@register.simple_tag()
def get_category_name(cat_id):
    cat_name = db.category_get_by_id(cat_id)["category_name"]
    if not cat_name:
        return ""
    return cat_name
