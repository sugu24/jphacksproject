from django.contrib import admin
from .models import UserModel, bookModel, readBooksModel, questionModel, languagesModel, junresModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(bookModel)
admin.site.register(readBooksModel)
admin.site.register(questionModel)
admin.site.register(languagesModel)
admin.site.register(junresModel)