from django.contrib import admin
from django.contrib import admin
from django.utils.html import format_html

from .models import Book, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'published_date', 'quantity', 'available_copies')
    search_fields = ('title', 'author', 'genre')
    list_filter = ('genre', 'published_date')
    readonly_fields = ('created_at', 'available_copies')

    def cover_image_tag(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="50" />', obj.cover_image.url)
        return "-"

    cover_image_tag.short_description = 'Cover'

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'return_date', 'status')
    search_fields = ('user__username', 'book__title')
    list_filter = ('status', 'borrow_date', 'due_date')
    readonly_fields = ('borrow_date',)

