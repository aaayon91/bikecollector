from django.contrib import admin
from .models import Bike, Order, Component

# Register your models here.
admin.site.register(Bike)
admin.site.register(Order)
admin.site.register(Component)