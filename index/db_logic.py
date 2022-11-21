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


def crop_create(name: str, desc: str, price: float, amount: int, origin: str,
                year: int, p_type: str, category: int, farmer: int):
    crop = models.Crop.objects.create(crop_name=name, description=desc, price=price,
                                      amount=amount, origin=origin, crop_year=year,
                                      price_type=p_type, category_id=category, farmer_id=farmer)
    if not crop:
        return False
    else:
        return crop


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


def get_list_of_categories():
    list_of_categories = []
    categories_models = get_all_categories()

    for category_model in categories_models:
        record = category_model['id'], category_model['category_name']
        list_of_categories.append(record)

    return list_of_categories


def crop_get_by_id(crop_id: int):
    try:
        crop = models.Crop.objects.get(id=crop_id)
    except exceptions.ObjectDoesNotExist:
        return False

    crop_dict = to_dict(crop)
    return crop_dict


def category_get_by_id(category_id):
    try:
        cat = models.Categories.objects.get(id=category_id)
    except exceptions.ObjectDoesNotExist:
        return False

    return to_dict(cat)


def get_subcategories(crop_category: int):
    open_list = []
    try:
        childs = models.Categories.objects.filter(category_of_id_id=crop_category)
        for child in childs.values():
            open_list.append(child['id'])
        return open_list

    except exceptions.ObjectDoesNotExist:
        return open_list


def crop_get_by_category(crop_category: int):
    crops_list = []
    new_list = [crop_category]
    i = 0

    open_list = get_subcategories(crop_category)

    while len(open_list) > 0:
        new_list.append(open_list[i])
        open_list.extend(get_subcategories(open_list[i]))
        open_list.reverse()
        open_list.pop()
        i+1

    while [] in new_list:
        new_list.remove([])

    for crops_category in new_list:
        try:
            children = models.Crop.objects.filter(category_id=crops_category)
        except exceptions.ObjectDoesNotExist:
            return

        for crop in children.values():
            if crop is not []:
                crops_list.append(crop)

    return crops_list


def harvest_get_by_id(harvest_id: int):
    try:
        harvest = models.Harvest.objects.get(id=harvest_id)
    except exceptions.ObjectDoesNotExist:
        return False

    return to_dict(harvest)


def harvest_get_all():
    db_harvests = models.Harvest.objects.all()
    if not db_harvests:
        return False

    harvests = []
    for harvest in db_harvests:
        harvests.append(to_dict(harvest))

    return harvests
