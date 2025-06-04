from django.contrib import admin

from .models import Category, Comment, Item, Purchase

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Purchase)
admin.site.register(Comment)
