import re
from . import db_logic as db


def try_cookie(request, cookie):
    """
    This function will test if cookie was set in dictionary
    If not it will create it (set to None) so it can be accessed
    """
    try:
        return request.COOKIES[cookie]
    except KeyError:
        return ""


def add_to_cart(request, crop_id, amount):
    cart = try_cookie(request, "cart")
    if cart is None:
        cart = f"{crop_id}:{amount};"
    else:
        if str(crop_id) in cart:
            pattern = f"{crop_id}:\d+;"
            cart = re.sub(pattern, f"{crop_id}:{amount};", cart)
        else:
            cart += f"{crop_id}:{amount};"
    return cart


def delete_from_cart(request, crop_id):
    cart = try_cookie(request, "cart")
    if cart is None:
        return
    pattern = f"{crop_id}:\d+;"
    cart = re.sub(pattern, "", cart)
    return cart


def get_cart(request, cart=None):
    if cart is None:
        cart = try_cookie(request, "cart")
        if cart is None:
            return False

    orders = []
    if cart == "":
        return orders

    items = cart.split(";")[:-1]
    for item in items:
        item = item.split(":")
        crop_id = int(item[0])     # get rid of the ':'
        crop = db.crop_get_by_id(crop_id)
        crop_name = crop["crop_name"]
        amount = int(item[1])
        price = crop["price"] * amount
        orders.append({"id": crop_id, "name": crop_name,
                       "amount": amount, "price": price})

    return orders
