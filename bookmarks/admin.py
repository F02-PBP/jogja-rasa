from django.contrib import admin
from .models import Bookmark

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'created_at')
    search_fields = ('user__username', 'restaurant__name')
    list_filter = ('created_at',)
