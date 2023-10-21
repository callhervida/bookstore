from django.contrib import admin

from book.models import Book, Comment


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'quantity', 'price')
    search_fields = ('title',)
    ordering = ['title', ]
    raw_id_fields = ('author',)


admin.site.register(Book, BookAdmin)
admin.site.register(Comment)
