# Generated by Django 4.1.3 on 2022-12-03 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
