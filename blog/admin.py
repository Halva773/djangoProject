from django.contrib import admin

from blog.models import Post, Categories

admin.site.register(Post)
admin.site.register(Categories)
