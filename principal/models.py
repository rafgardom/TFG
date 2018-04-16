from django.db import models

# Create your models here.
class Order(models.Model):
    order_type = models.CharField("Order type", unique=True, max_length= 4)

    def __unicode__(self):
        return self.order_type

class Sort(models.Model):
    sort_type = models.CharField("Sort type", unique=True, max_length=10)
    spanish_name = models.CharField("Spanish name", unique=True, max_length=10)

    def __unicode__(self):
        return self.spanish_name