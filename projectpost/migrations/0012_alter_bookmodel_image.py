# Generated by Django 3.2.7 on 2021-10-25 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0011_auto_20211025_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='image',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
