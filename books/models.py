from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.defaultfilters import slugify

from shelves.models import Shelve
# Create your models here.

User = get_user_model()

class Book(models.Model):
    shelve = models.ForeignKey(Shelve, on_delete=models.SET_NULL, null=True)
    creature = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField(User, related_name='authores')
    name = models.CharField(max_length=25)
    publish = models.BooleanField(default=False)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='media/images/books', default='media/images/default.jpg')

    
    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse("books-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Shelve, self).save(*args, **kwargs)


class BookTag(models.Model):
    name = models.CharField(max_length=15)
    books = models.ManyToManyField(Book)
