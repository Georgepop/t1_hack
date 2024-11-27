from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    language = models.CharField(max_length=32)
    access = models.CharField(max_length=32)
