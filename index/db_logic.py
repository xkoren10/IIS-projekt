from django.db import connection
import django.contrib.auth.hashers as hasher
from . import models
import django.core.exceptions as exceptions
from itertools import chain


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


def user_get_by_id(user_id: int):
    try:
        user = models.User.objects.get(id=user_id)
    except exceptions.ObjectDoesNotExist:
        return False

    user_dict = to_dict(user)
    return user_dict


def user_create(username: str, password: str, email=''):
    try:
        user_exists = models.User.objects.get(user_name=username)
    except exceptions.ObjectDoesNotExist:

        psw_hash = hasher.make_password(password)
        user = models.User.objects.create(user_name=username, email=email, password=psw_hash, mod=False)
        return user

    if user_exists:
        # now this would be bad
        return False


def user_delete(user_id: int):
    try:
        models.User.objects.filter(id=user_id).delete()
    except exceptions.ObjectDoesNotExist:
        return False

    return True


def user_update(user_id: int, user_name: str, email: str, password: str, mod: bool):
    try:
        models.User.objects.filter(id=user_id).update(user_name=user_name, password=hasher.make_password(password), email=email, mod=mod)
    except exceptions.ObjectDoesNotExist:
        return False

    return True


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


def get_crops_from_farmer(farmer_id: int):
    farmers_crops = []
    farmers_crops_models = models.Crop.objects.filter(farmer_id=farmer_id)
    if not farmers_crops_models:
        return False
    for crop in farmers_crops_models:
        farmers_crops_dict = to_dict(crop)
        farmers_crops.append(farmers_crops_dict)

    return farmers_crops


def get_top_crops():
    top_crops = []
    top_crops_models = models.Crop.objects.filter(review__stars__gte=4).order_by('-review__stars')[:2]
    # nech to neni crowded
    if not top_crops_models:
        return False

    for crop in top_crops_models:
        top_crops_dict = to_dict(crop)
        top_crops.append(top_crops_dict)

    return top_crops


def get_new_crops():
    new_crops = []
    new_crops_models = models.Crop.objects.order_by('crop_year')[:2]
    # nech to neni crowded
    if not new_crops_models:
        return False

    for crop in new_crops_models:
        new_crops_dict = to_dict(crop)
        new_crops.append(new_crops_dict)

    return new_crops


def get_all_crops():
    all_crops = []
    all_crops_models = models.Crop.objects.all()

    if not all_crops_models:
        return False

    for crop in all_crops_models:
        all_crops_dict = to_dict(crop)
        all_crops.append(all_crops_dict)

    return all_crops


def get_all_categories():
    all_categories = []
    all_categories_models = models.Categories.objects.all()

    if not all_categories_models:
        return False

    for crop in all_categories_models:
        all_categories_dict = to_dict(crop)
        all_categories.append(all_categories_dict)

    return all_categories


def crop_get_by_id(crop_id: int):
    try:
        crop = models.Crop.objects.get(id=crop_id)
    except exceptions.ObjectDoesNotExist:
        return False

    crop_dict = to_dict(crop)
    return crop_dict


def crop_get_by_category(crop_category: int): # tu potrebujeme tree hierarchy z mptt, nvm ako

    try:
        childs = models.Categories.objects.filter(category_of_id_id=crop_category) | models.Categories.objects.filter(id=crop_category)
    except exceptions.ObjectDoesNotExist:
        return childs

    for child in childs:
        childs = crop_get_by_category(child['id'])

    crop_dict = to_dict(childs)
    return crop_dict
