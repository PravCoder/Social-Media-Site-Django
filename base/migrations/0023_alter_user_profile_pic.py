# Generated by Django 3.2.19 on 2023-08-20 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.FileField(null=True, upload_to='images/'),
        ),
    ]
