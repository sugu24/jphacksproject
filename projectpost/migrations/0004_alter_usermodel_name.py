# Generated by Django 3.2.7 on 2021-10-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0003_auto_20211023_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
