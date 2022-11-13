# This file contains objects for database
from . import db_logic as db
from django.db import models


class User(models.Model):

    user_name = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    mod = models.BooleanField


class Categories(models.Model):

    category_name = models.CharField(max_length=90)
    category_of_id = models.ForeignKey('self', on_delete=models.CASCADE)


class Crop(models.Model):

    crop_name = models.CharField(max_length=80)
    description = models.CharField(max_length=80)
    price = models.FloatField()
    weight = models.FloatField()
    pieces = models.IntegerField()
    origin = models.CharField(max_length=80)
    crop_year = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price_type = models.CharField(max_length=5,
                                  choices=[
                                      ("perpc", "per piece"),
                                      ("perkg", "per kilogram")
                                  ],
                                  default="perkg"
                                  )
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):

    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_by')
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer')
    total_price = models.FloatField()
    amount = models.IntegerField()
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)


class Harvest(models.Model):

    date = models.DateField()
    place = models.CharField(max_length=80)
    description = models.CharField(max_length=80)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):

    short_desc = models.CharField(max_length=80)
    long_desc = models.CharField(max_length=200)
    stars = models.IntegerField()
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE)





