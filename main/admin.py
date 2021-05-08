from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserList
# from .models import Youtube
# from embed_video.admin import AdminVideoMixin
#
#
# class YoutubeAdmin(AdminVideoMixin, admin.ModelAdmin):
#     vid_display = ('video', 'slug')
#
#
# admin.site.register(Youtube, YoutubeAdmin)

# Register your models here.
from .models import ReviewsList


@admin.register(ReviewsList)
class RequestReviewAdmin(admin.ModelAdmin):
    list_display = ["review"]

# @admin.register(UserList)
# class RequestDemoAdmin(admin.ModelAdmin):
#     list_display = ["title", "genre", "rating"]