from django.db import models
from django.db.models.expressions import F
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

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
    
    
    
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_session"
        
class SystemLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(null=True, blank=True)
    session_id = models.TextField(null=True, blank=True)
    loggedin_at = models.DateTimeField(auto_now_add=True)
    loggedout_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'system_log'
