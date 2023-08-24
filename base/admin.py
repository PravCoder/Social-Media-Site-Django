from django.contrib import admin
from.models import User, Post, Comment, DirectMessage, DirectMessageChat


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(DirectMessageChat)
admin.site.register(DirectMessage)