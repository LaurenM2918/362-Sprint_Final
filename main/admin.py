from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import ReviewsList

@admin.register(ReviewsList)
class RequestReviewAdmin(admin.ModelAdmin):
    list_display = ["review"]