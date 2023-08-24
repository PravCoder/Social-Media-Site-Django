# Generated by Django 3.2.8 on 2023-07-16 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_auto_20230716_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.FileField(null=True, upload_to='images/'),
        ),
    ]