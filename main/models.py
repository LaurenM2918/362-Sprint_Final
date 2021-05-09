from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# # Profile Model
# class MyModel(models.Model):
#     id = models.AutoField(null=False, primary_key=True)
#     user_name = models.CharField(max_length=255, null=False)
#     first_name = models.CharField(max_length=255, null=False)
#     last_name = models.CharField(max_length=255, null=False)
#     email = models.CharField(max_length=255, null=False)
#     password1 = models.CharField(max_length=255, null=False)


# Log In Model
class UserLogin(models.Model):
    username = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.username


# User List Model
class UserList(models.Model):
    id = models.AutoField(null=False, primary_key=True)
    title = models.CharField(max_length=255, null=True)
    genre = models.CharField(max_length=255, null=True)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])


# UI List
class UIList(models.Model):
    id = models.AutoField(null=False, primary_key=True)
    title = models.CharField(max_length=255, null=True)
    genre = models.CharField(max_length=255, null=True)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])

# Reviews List
class ReviewsList(models.Model):
    id = models.AutoField(null=False, primary_key=True)
    review = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.review

