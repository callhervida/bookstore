from django.contrib import admin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from book.models import Book, Comment
from user.models import User


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'quantity', 'price', 'author', 'id')
    search_fields = ('title',)
    ordering = ['title', ]

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]


admin.site.register(Book, BookAdmin)
admin.site.register(Comment)
