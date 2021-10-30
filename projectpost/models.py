from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='', default='ヒントからの最終盤面1.png')
    bio = models.CharField(max_length=300, null=True, blank=True)
    junres = models.CharField(max_length=1000, null=True, blank=True)
    languages = models.CharField(max_length=1000, null=True, blank=True)
    favorite_books = models.CharField(max_length=1000, null=True, blank=True)


class bookModel(models.Model):
    name = models.CharField(max_length=100)
    ibsn = models.CharField(max_length=15, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)
    junre = models.CharField(max_length=20, null=True, blank=True)
    diff1 = models.IntegerField(null=True, blank=True, default=0)
    diff2 = models.IntegerField(null=True, blank=True, default=0)
    diff3 = models.IntegerField(null=True, blank=True, default=0)
    diff4 = models.IntegerField(null=True, blank=True, default=0)
    diff5 = models.IntegerField(null=True, blank=True, default=0)


class readBooksModel(models.Model):
    reader = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name = "readerOf")
    book = models.ForeignKey(bookModel, on_delete=models.CASCADE, related_name="readBookOf")
    thoughts = models.TextField()
    value = models.IntegerField()
    lower_diff = models.IntegerField()
    upper_diff = models.IntegerField()
    order_language = models.IntegerField(null=True, blank=True)
    order_junre = models.IntegerField(null=True, blank=True)


class questionModel(models.Model):
    profile = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="profileOf")
    room = models.CharField(max_length=40, blank=True, null=True)
    question = models.TextField()


class answerModel(models.Model):
    profile = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    response_to = models.ForeignKey(questionModel, on_delete=models.CASCADE)
    answer = models.TextField()


class languagesModel(models.Model):
    language = models.CharField(max_length=200, null=True, blank=True, default="C C++ C# Python JavaScript")


class junresModel(models.Model):
    junres = models.CharField(max_length=200, default="django llvm agax")