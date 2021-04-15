from django.db import models


# Profile Model
class MyModel(models.Model):
    id = models.AutoField(null=False, primary_key=True)
    user_name = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    password1 = models.CharField(max_length=255, null=False)
    password2 = models.CharField(max_length=255, null=False)