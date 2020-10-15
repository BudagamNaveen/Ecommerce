from django.contrib import admin
from .models import (Products,
	Order,
	OrderItem,
	Billing_Address,
	Maincategories,
	Subcategories)

# Register your models here.
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Billing_Address)
admin.site.register(Maincategories)
admin.site.register(Subcategories)