# Generated by Django 4.1.3 on 2022-12-26 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstack', '0009_book_thumbnail_shelve_thumbnail_alter_book_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='publish',
            new_name='published',
        ),
    ]
