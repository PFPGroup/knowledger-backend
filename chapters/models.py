from django.db import models
from django.contrib.auth import get_user_model

from books.models import Book
# Create your models here.

User = get_user_model()

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)


class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    text = models.TextField()


class PageImage(models.Model):
    image = models.ImageField(upload_to='media/images/pages', default='media/images/default.jpg')
    page = models.ManyToManyField(Page)


class Activity(models.Model):
    
    ACTIVITY_TYPE = (
        (1, 'Book'),
        (2, 'Page'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(choices=ACTIVITY_TYPE, max_length=1)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    Page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)