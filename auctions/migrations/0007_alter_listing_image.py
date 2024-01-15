# Generated by Django 4.2.9 on 2024-01-15 07:09

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_comment_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, default='https://react.semantic-ui.com/images/image-16by9.png', max_length=255, verbose_name='images/'),
        ),
    ]
