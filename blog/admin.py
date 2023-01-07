from django.contrib import admin
from django.contrib.admin.options import TabularInline
from .models import ArticleImage, Article
# Register your models here.
class ImageAdminInline(TabularInline):
    extra = 1
    model = ArticleImage
    readonly_fields=("image_detail",)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines= (ImageAdminInline,)
    list_display=("title","owner","is_visible","view_count","created_time")
    list_filter=("owner","created_time")
    search_fields= ("created_time",)
    readonly_fields= ('image_detail','view_count','created_time','updated_time')
    
@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'image','image_detail')
    fields=("article","image_detail")
    readonly_fields= ('image_detail',)