from django.contrib import admin

# Register your models here.
from .models import MyModel


@admin.register(MyModel)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = ["user_name", "first_name", "last_name", "email", "password1", "password2"]
