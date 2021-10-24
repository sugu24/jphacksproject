from django.contrib import admin
from .models import UserModel, bookModels, readBooksModels, postModels, languagesModels, junresModels

# Register your models here.
admin.site.register(UserModel)
admin.site.register(bookModels)
admin.site.register(readBooksModels)
admin.site.register(postModels)
admin.site.register(languagesModels)
admin.site.register(junresModels)