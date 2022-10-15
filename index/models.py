# This file contains models for database
# admin username and password is 'admin'

from django.db import models


class CropCategory(models.Model):
    """
    Category of a crop
    It should have a name and parent category
    """
    name = models.CharField(max_length=50)
    # recursion in databases? what's next? blacks owning property?
    category_of = models.ForeignKey('self', on_delete=models.CASCADE)


class Crop(models.Model):
    """
    Crop is some kind of veggie or fruit
    It should have a name, prize and available amount
    """
    name = models.CharField(max_length=100)
    prize = models.IntegerField()
    prize_type = models.CharField(max_length=5,
                                  choices=[
                                      ("perpc", "per piece"),
                                      ("perkg", "per kilogram")
                                  ],
                                  default="perkg"
                                  )
    amount = models.IntegerField()
    category = models.ForeignKey(CropCategory, on_delete=models.CASCADE)


class User(models.Model):
    """
    User model
    Idk, might be completely wrong to use it here in models to push it into db
    """
    name = models.CharField(max_length=100)


class Harvest(models.Model):
    """
    Model for harvest organized by farmers
    """
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    place = models.CharField(max_length=100)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)


class Order(models.Model):
    """
    Order contains info about bought crops
    Should contain user who ordered, farmer who sold, bought crops, amount and total prize
    """
    order_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordered_by")
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="farmer")
    crop = models.ManyToManyField(Crop)
    amount = models.IntegerField()
    total_prize = models.IntegerField()
