from django.db import models

class Product(models.Model):

    brand = models.CharField(max_length=100, null=False)
    group = models.CharField(max_length=100, null=False)
    old_price = models.CharField(max_length=100, null=True)
    discount = models.CharField(max_length=100, null=True)
    new_price = models.CharField(max_length=100, null=True)
    fullprice = models.CharField(max_length=100, null=True)
    sizes = models.CharField(max_length=100, null=True)
    colors = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=200, null=False)
    art = models.CharField(max_length=100, null=False)


