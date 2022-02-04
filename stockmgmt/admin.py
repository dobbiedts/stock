from django.contrib import admin
from .models import *
from .forms import StockCreateForm
# Register your models here.

#customising admin page
class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['category', 'item_name', 'quantity', 'issue_by', 'reorder_level']
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']

admin.site.register(Stock, StockCreateAdmin)

