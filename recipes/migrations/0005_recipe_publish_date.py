# Generated by Django 4.1.2 on 2022-10-10 22:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0004_alter_recipe_image_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='publish_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
