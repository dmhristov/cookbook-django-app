from django.contrib import admin

from cookbook.main.models import Recipe, Like, Comment, Reply


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'recipe', 'author']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['text', 'comment', 'author']
