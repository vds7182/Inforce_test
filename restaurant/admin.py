from django.contrib import admin
from restaurant.models import Menu,MenuItem,Restaurant

# Register your models here.
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Restaurant)