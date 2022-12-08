from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

# Create your models here.

User = get_user_model()

class Shelve(models.Model):
    creature = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True,max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/images/shelves', default='media/images/default.jpg')
    tags = TaggableManager()


    class Meta:
        ordering = ('-name',)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    shelve = models.ForeignKey(Shelve, on_delete=models.SET_NULL, null=True, related_name='books')
    creature = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField(User, related_name='authors')
    name = models.CharField(max_length=25)
    publish = models.BooleanField(default=False)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='media/images/books', default='media/images/default.jpg')
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-name',)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapter')
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self) -> str:
        return self.name

class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='page')
    name = models.CharField(max_length=150, null=True) # in deployment change null to False
    text = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class PageImage(models.Model):
    image = models.ImageField(upload_to='media/images/pages', default='media/images/default.jpg')
    page = models.ManyToManyField(Page)


class PageReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='reviews', default=None) # remove the default in deployment
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)


class Activity(models.Model):

    class ActivityType(models.TextChoices):
        CREATED = 1
        UPDATED = 2
        DELETED = 3
    
    class ModelType(models.TextChoices):
        SHELVE = 'shelve'
        BOOK = 'book'
        PAGE = 'page'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(choices=ActivityType.choices, max_length=1)
    model_type = models.CharField(choices=ModelType.choices, max_length=6)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    Shelve = models.ForeignKey(Shelve, on_delete=models.CASCADE, null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)