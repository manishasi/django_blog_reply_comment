from django.contrib import admin
from .models import Profile, Post,Comment,Reply



# class imageAdmin(admin.ModelAdmin):
#     list_display = ["title","image", "likes","dislikes"]

admin.site.register(Profile)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["views","image","title"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author","comment_body","post"]

@admin.register(Reply)
 
class ReplyAdmin(admin.ModelAdmin):
     list_display = ["comment","reply_body","author"]
