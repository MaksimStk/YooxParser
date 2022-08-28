from django.contrib import admin
from .models import Product
from .forms import ProductForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'group', 'old_price', 'discount', 'new_price', 'fullprice', 'sizes', 'colors', 'link', 'art')
    form = ProductForm


