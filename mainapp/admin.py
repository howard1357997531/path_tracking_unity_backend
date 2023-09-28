from django.contrib import admin
from .models import *

@admin.register(Object_3d)
class object_3dAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Route)
class routeAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_3d', 'points')