from django.db import models
from django.db.models.expressions import F

# Create your models here.
category_choice = (
		('Furniture', 'Furniture'),
		('IT Equipment', 'IT Equipment'),
		('Phone', 'Phone'),
        ('Car', 'Car'),
        ('Record', 'Record'),
	)


class Stock(models.Model):
    category = models.CharField(max_length = 50, blank = True, null = True, choices = category_choice)
    item_name = models.CharField(max_length = 50, blank = True, null = True)
    quantity = models.IntegerField(default = '0', blank = True, null = True)
    receive_quantity = models.IntegerField(default = '0', blank = True, null = True)
    receive_by = models.CharField(max_length = 50, blank = True, null = True)
    issue_quantity = models.IntegerField(default = '0', blank = True, null = True)
    issue_by = models.CharField(max_length= 50, blank= True, null = True)
    issue_to = models.CharField(max_length= 50, blank = True, null =True)
    phone_number= models.CharField(max_length= 50, blank = True, null =True)
    created_by = models.CharField(max_length= 50, blank = True, null =True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add= False, auto_now = True)
    timestamp = models.DateTimeField(auto_now_add= True, auto_now = False)

    def __str__(self):
        return self.item_name + ' ' + str(self.quantity)


class StockHistory(models.Model):
    category = models.CharField(max_length = 50, blank = True, null = True, choices = category_choice)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)