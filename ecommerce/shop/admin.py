from django.contrib import admin

from shop.models import Category
admin.site.register(Category)

from shop.models import Products
admin.site.register(Products)
