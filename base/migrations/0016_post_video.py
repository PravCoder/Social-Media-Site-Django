# Generated by Django 3.2.8 on 2023-07-16 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20230519_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='upload/'),
        ),
    ]
