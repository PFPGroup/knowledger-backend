from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Shelve(models.Model):
    creature = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    creature = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField(User, related_name='authores')
    name = models.CharField(max_length=25)
    publishable = models.BooleanField(default=False)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=15)
    books = models.ManyToManyField(Book)