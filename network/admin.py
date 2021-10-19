from django.contrib import admin
from .models import Following, User, Post, Like
# Register your models here.


# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Like)
