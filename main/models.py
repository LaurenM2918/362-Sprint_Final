from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# from embed_video.fields import EmbedVideoField


# Log In Model
class UserLogin(models.Model):
    username = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __unicode__(self):
        return self.username


# User List Model
class UserList(models.Model):
    objects = None
    id = models.AutoField(null=False, primary_key=True)
    title = models.CharField(max_length=255, null=True)
    genre = models.CharField(max_length=255, null=True)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __unicode__(self):
        return self.title


class ReviewsList(models.Model):
    id = models.AutoField(null=False, primary_key=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.review


# # Youtube Database Model
# class Youtube(models.Model):
#     objects = None
#     video = EmbedVideoField()
#     slug = models.SlugField(max_length=200, db_index=True, unique=True)
#
#     def __str__(self):
#         return self.video