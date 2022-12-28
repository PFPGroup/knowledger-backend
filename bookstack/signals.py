from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

from bookstack.models import Shelve

@receiver(pre_save, sender=Shelve)
def pre_save_shelve(sender, instance, *args, **kwargs):
    try:
        old_obj = instance.__class__.objects.get(id=instance.id)
        try:
            new_image_path = instance.image.path
            new_thumbnail_path = instance.thumbnail.path
        except:
            new_image_path = None
            new_thumbnail_path = None
        if new_image_path != old_obj.image.path:
            if os.path.exists(old_obj.image.path):
                os.remove(old_obj.image.path)
        if new_thumbnail_path != old_obj.thumbnail.path:
            if os.path.exists(old_obj.thumbnail.path):
                os.remove(old_obj.thumbnail.path)
    except:
        pass