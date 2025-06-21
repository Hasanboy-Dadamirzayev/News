from django.contrib import admin
from .models import *
from django.utils.html import mark_safe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

class ContentInline(admin.StackedInline):
    model = Content
    extra = 1

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'author', 'reading_time', 'view', 'created_at', 'published', 'important', 'category', 'comments')
    search_fields = ['title', 'author', 'intro']
    list_filter = ('author', 'important', 'published', 'category')
    inlines = [ContentInline, CommentInline]


    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="140px" height="100px"/>')
        return "(No image)"

@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'photo_tag', 'created_at', 'published')
    list_filter = ('author', 'published',)
    search_fields = ('title',)




    def photo_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.photo.url}" width="140px" height="100px"/>')
        return "(No image)"




