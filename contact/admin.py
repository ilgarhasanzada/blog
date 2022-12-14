from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'phone', 'message')