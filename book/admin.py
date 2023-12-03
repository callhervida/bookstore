from django.contrib import admin
from django.db import models

from django.contrib.admin.helpers import ActionForm
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.admin import GenericTabularInline

from book.models import Book, Comment
from user.models import User
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.contrib import admin
# from .models import DynamicForm, DynamicFormField
# from django.forms.models import BaseInlineFormSet, modelform_factory
# from .models import DynamicForm, DynamicFormField
# from .models import FormData, FormFieldData


# class DynamicFormFieldInlineFormSet(BaseInlineFormSet):
#     def get_formset(self, request, obj=None, **kwargs):
#         if obj:
#             # Filter fields based on the selected DynamicForm
#             fields = ('field_type', 'label', 'value_file')  # Add other fields as needed
#             self.form = modelform_factory(DynamicFormField, fields=fields)
#         return super().get_formset(request, obj=obj, **kwargs)
#
#
# class DynamicFormFieldInline(admin.TabularInline):
#     model = DynamicFormField
#     extra = 1
#     formset = DynamicFormFieldInlineFormSet
#
#
# @admin.register(DynamicForm)
# class DynamicFormAdmin(admin.ModelAdmin):
#     inlines = [DynamicFormFieldInline]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'quantity', 'price', 'author', 'id')
    search_fields = ('title',)
    ordering = ['title', ]


# class FormFieldDataInline(admin.TabularInline):
#     model = FormFieldData
#     extra = 1
#
#
# @admin.register(FormData)
# class FormDataAdmin(admin.ModelAdmin):
#     inlines = [FormFieldDataInline]
#
#
# # admin.site.register(FormData, FormDataAdmin)
# admin.site.register(FormFieldData)


admin.site.register(Comment)
admin.site.register(Book, BookAdmin)
