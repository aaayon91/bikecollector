from django.contrib import admin
from .models import Bike, Order, Component, Photo

# Register your models here.
admin.site.register(Bike)
admin.site.register(Order)
admin.site.register(Component)
admin.site.register(Photo)