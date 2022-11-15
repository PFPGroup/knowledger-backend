from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.

User = get_user_model()

class Shelve(models.Model):
    creature = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True,max_length=50)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/images/shelves', default='media/images/default.jpg')


    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse("shelve-detail", kwargs={"pk": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Shelve, self).save(*args, **kwargs)