from django.contrib import admin
from .models import Ilan

# Register your models here.

@admin.register(Ilan)
class IlanAdmin(admin.ModelAdmin):
    list_display = ["title", "created_date"]
    list_display_links = ["title"]
    search_fields = ["title"]
    list_filter = ["created_date"]