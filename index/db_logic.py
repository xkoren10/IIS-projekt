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


def crop_update(crop_id: int, name: str, desc: str, price: float, amount: int, origin: str,
                year: int, p_type: str, category: int, farmer: int):
    crop = models.Crop.objects.filter(id=crop_id).update(crop_name=name, description=desc, price=price,
                                        amount=amount, origin=origin, crop_year=year,
                                        price_type=p_type, category_id=category, farmer_id=farmer)
    if not crop:
        return False
    else:
        return crop


def crop_delete(crop_id: int):
    try:
        models.Crop.objects.filter(id=crop_id).delete()
    except exceptions.ObjectDoesNotExist:
        return False

    return True


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
    new_crops_models = models.Crop.objects.order_by('-crop_year', '-id')[:2]
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


def crop_delete(crop_id: int):
    try:
        models.Crop.objects.filter(id=crop_id).delete()
    except exceptions.ObjectDoesNotExist:
        return False

    return True


def get_all_categories():
    all_categories = []
    all_categories_models = models.Categories.objects.all().order_by("id")

    if not all_categories_models:
        return False

    for crop in all_categories_models:
        all_categories_dict = to_dict(crop)
        all_categories.append(all_categories_dict)

    return all_categories


def get_list_of_categories():
    list_of_categories = []
    categories_models = category_get_all_approved()

    if not categories_models:
        return False

    for category_model in categories_models:
        record = category_model['id'], category_model['category_name']
        list_of_categories.append(record)

    return list_of_categories


def get_list_of_farmers_crops(farmer_id: int):
    list_of_crops = []
    crops_dict = get_crops_from_farmer(farmer_id)

    if not crops_dict:
        return False
    for crop in crops_dict:
        record = crop['id'], crop['crop_name']
        list_of_crops.append(record)

    return list_of_crops


def crop_get_by_id(crop_id: int):
    try:
        crop = models.Crop.objects.get(id=crop_id)
    except exceptions.ObjectDoesNotExist:
        return False

    crop_dict = to_dict(crop)
    return crop_dict


def category_get_by_id(category_id: int):
    try:
        cat = models.Categories.objects.get(id=category_id)
    except exceptions.ObjectDoesNotExist:
        return False

    return to_dict(cat)


def category_approved(category_id: int, approve=True):
    try:
        if approve:
            models.Categories.objects.filter(id=category_id).update(approved=True)
        else:
            models.Categories.objects.filter(id=category_id).update(approved=False)
    except exceptions.ObjectDoesNotExist:
        return False


def category_get_all_approved():
    approved_db = models.Categories.objects.filter(approved=True)
    if not approved_db:
        return False

    approved_cats = []
    for approved in approved_db:
        approved_cats.append(to_dict(approved))

    return approved_cats


def category_delete(cat_id: int):
    try:
        models.Categories.objects.filter(id=cat_id).delete()
    except exceptions.ObjectDoesNotExist:
        return False

    return True


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

    open_list = get_subcategories(crop_category)

    while len(open_list) > 0:
        new_list.append(open_list[0])
        open_list.extend(get_subcategories(open_list[0]))
        open_list.reverse()
        open_list.pop()

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


def harvests_attended(attendee_id: int):
    user_harvests = []
    all_harvests = models.Harvest.objects.filter(attendees__in=[attendee_id])
    for harvest in all_harvests:
        user_harvests.append(to_dict(harvest))
    return user_harvests


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
        harvest_dict = to_dict(harvest)
        harvest_dict["crop"] = crop_get_by_id(harvest_dict["crop"])["crop_name"]
        harvest_dict["farmer"] = user_get_by_id(harvest_dict["farmer"])["user_name"]
        harvests.append(harvest_dict)

    return harvests


def harvest_delete(harvest_id):
    try:
        models.Harvest.objects.filter(id=harvest_id).delete()
    except exceptions.ObjectDoesNotExist:
        return False

    return True


def get_order_by_person_id(person_id: int):
    order_list = []
    try:
        order_models = models.Order.objects.all().filter(farmer_id=person_id) or models.Order.objects.all().filter(ordered_by=person_id)
    except exceptions.ObjectDoesNotExist:
        return False

    for order_model in order_models:
        order_dict = to_dict(order_model)
        order_dict["ordered_by"] = user_get_by_id(order_dict["ordered_by"])["user_name"]
        order_dict["crop"] = crop_get_by_id(order_dict["crop"])["crop_name"]
        order_list.append(order_dict)

    return order_list


def create_new_orders(user_id: int, crops):
    for crop in crops:
        crop_id = crop["id"]
        db_crop = crop_get_by_id(crop_id)
        farmer_id = user_get_by_id(db_crop["farmer"])["id"]
        amount = crop["amount"]
        total_price = float(crop["price"])
        state = "pending"
        order = models.Order.objects.create(crop_id=crop_id, farmer_id=farmer_id, ordered_by_id=user_id,
                                            amount=amount, total_price=total_price, state=state)


def change_order_state(state: str, order_id: int):
    order = models.Order.objects.filter(id=order_id).update(state=state)
    if order:
        return
    else:
        return False
