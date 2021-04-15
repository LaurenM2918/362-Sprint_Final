from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import UserList


@admin.register(UserList)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "rating"]