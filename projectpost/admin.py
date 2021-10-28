from django.contrib import admin
from .models import UserModel, bookModel, readBooksModel, postModel, languagesModel, junresModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(bookModel)
admin.site.register(readBooksModel)
admin.site.register(postModel)
admin.site.register(languagesModel)
admin.site.register(junresModel)