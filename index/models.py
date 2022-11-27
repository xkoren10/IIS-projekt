# This file contains objects for database
from . import db_logic as db
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from itertools import chain
# from mptt.models import MPTTModel, TreeForeignKey


class User(models.Model):

    user_name = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    mod = models.BooleanField(default=False)


class Categories(models.Model):

    category_name = models.CharField(max_length=90)
    category_of_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    approved = models.BooleanField(default=False)


class Crop(models.Model):

    crop_name = models.CharField(max_length=80)
    description = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.PositiveIntegerField()
    origin = models.CharField(max_length=80)
    crop_year = models.DateField(null=True)
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
    total_price = models.FloatField(MinValueValidator(0.0))
    amount = models.PositiveIntegerField()
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    state = models.CharField(max_length=10,
                             choices=[("pen", "pending"), ("rej", "rejected"), ("con", "confirmed")],
                             default="pending")


class Harvest(models.Model):

    date = models.DateField()
    place = models.CharField(max_length=80)
    description = models.CharField(max_length=80)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    max_occupancy = models.PositiveIntegerField(default=0)
    current_occupancy = models.PositiveIntegerField(default=0)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='harvest_farmer')
    attendees = models.ManyToManyField(User)


class Review(models.Model):

    short_desc = models.CharField(max_length=80)
    long_desc = models.CharField(max_length=200)
    stars = models.PositiveIntegerField(MaxValueValidator(5))
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Admin(models.Model):
    login = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
