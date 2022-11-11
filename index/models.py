# This file contains objects for database
from . import db_logic as db


class User(object):
    def __init__(self, user_id, user_name, email, mod=False):
        self.id = user_id
        self.user_name = user_name
        self.email = email
        self.mod = mod


class Crop(object):
    """
    CROP SAMOZREJME NEMA LINK NA FARMARA/USERA
    """
    def __init__(self, crop_id, crop_name, weight, pieces, description, origin, crop_year, category_id, price_type):
        self.crop_id = crop_id
        self.crop_name = crop_name
        self.weight = weight
        self.pieces = pieces
        self.description = description
        self.origin = origin
        self.crop_year = crop_year
        self.category = category_id        # get_category_by_id
        self.price_type = price_type
        # self.farmer = db.user_get_by_id(farmer_id)


class Order(object):
    def __int__(self, order_id, ordered_by_user_id, farmer_id, total_price, amount, crop_id):
        self.order_id = order_id
        self.ordered_by = db.user_get_by_id(ordered_by_user_id)
        self.farmer = db.user_get_by_id(farmer_id)
        self.total_price = total_price
        self.amount = amount
        self.crop = crop_id         # db.get_crop_by_id(crop_id)


class Harvest(object):
    def __init__(self, harvest_id, date, place, description, crop_id, farmer_id):
        self.harvest_id = harvest_id
        self.date = date
        self.place = place
        self.description = description
        self.drop = crop_id         # db.get_crop_by_id(crop_id)
        self.farmer = db.user_get_by_id(farmer_id)


class Review(object):
    def __init__(self, review_id, short_desc, long_desc, stars, crop_id, user_id):
        self.review_id = review_id
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.stars = stars
        self.crop = crop_id         # db.get_crop_by_id(crop_id)
        self.reviewed_by = db.user_get_by_id(user_id)


class Categories(object):
    def __init__(self, category_id, category_name, category_of_id):
        self.category_id = category_id
        self.category_name = category_name
        self.category_of_id = category_of_id    # not from db, would be unwanted recursion with lots of objects linked together
