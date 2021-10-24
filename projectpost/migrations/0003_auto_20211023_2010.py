# Generated by Django 3.2.7 on 2021-10-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0002_auto_20211023_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='junres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('junres', models.CharField(default='django llvm agax', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(default='C C++ C# Python JavaScript', max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]