# Generated by Django 3.2.19 on 2023-08-20 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='media-images'),
        ),
    ]
