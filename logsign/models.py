from django.db import models

# Create your models here.
class sign(models.Model):
    name = models.CharField()
    phone_no = models.PositiveIntegerField()
    email = models.EmailField()
    password = models.CharField()
    confirm_password = models.CharField()
