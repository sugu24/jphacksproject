# Generated by Django 3.2.7 on 2021-10-24 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0005_auto_20211023_2025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='images',
            new_name='image',
        ),
    ]
