from typing import Any
from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )