from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='', default='ともや.JPG')
    bio = models.CharField(max_length=300, null=True, blank=True)
    junres = models.CharField(max_length=1000, null=True, blank=True)
    languages = models.CharField(max_length=1000, null=True, blank=True)
    favorite_books = models.CharField(max_length=1000, null=True, blank=True)


class bookModels(models.Model):
    name = models.CharField(max_length=100)
    page = models.IntegerField()
    language = models.CharField(max_length=20, null=True, blank=True)
    junre = models.CharField(max_length=20, null=True, blank=True)
    diff1 = models.IntegerField(null=True, blank=True, default=0)
    diff2 = models.IntegerField(null=True, blank=True, default=0)
    diff3 = models.IntegerField(null=True, blank=True, default=0)
    diff4 = models.IntegerField(null=True, blank=True, default=0)
    diff5 = models.IntegerField(null=True, blank=True, default=0)


class readBooksModels(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(bookModels, on_delete=models.CASCADE)
    thoughts = models.TextField()
    value = models.IntegerField()
    lower_diff = models.IntegerField()
    upper_diff = models.IntegerField()


class postModels(models.Model):
    profile = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book = models.ForeignKey(bookModels, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    to = models.IntegerField(null=True, blank=True, default=0)
    good = models.IntegerField(null=True, blank=True, default=0)


class languagesModels(models.Model):
    language = models.CharField(max_length=200, null=True, blank=True, default="C C++ C# Python JavaScript")


class junresModels(models.Model):
    junres = models.CharField(max_length=200, default="django llvm agax")