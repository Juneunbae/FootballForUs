from django.contrib import admin
from FBForUs.models import News, Comment, Reply
# Register your models here.

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Reply)