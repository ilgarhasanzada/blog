from django.contrib import admin
from django.contrib.admin.options import TabularInline
from .models import Contact,Post,ArticleImage
from django.template.loader import get_template
# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    readonly_fields= ('name','email','phone','message')
class ImageAdminInline(TabularInline):
    extra = 1
    model = ArticleImage
    # readonly_fields=("shows_image",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines= (ImageAdminInline,)
    list_display=("title","owner","visible","view_count","time")
    list_filter=("owner","time")
    search_fields= ("title",)
    readonly_fields= ('show_image','slug','view_count')
    
@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image','shows_image')
    fields=("post","shows_image")
    readonly_fields= ('shows_image',)