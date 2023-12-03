from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from django.db import models
from user.models import User
from django.db.models import Count, Avg, JSONField

from bookstore import settings


# class DynamicField(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True,)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=1)
#     object_id = models.PositiveIntegerField(blank=True, null=True,)
#     content_object = GenericForeignKey('content_type', 'object_id')
#     value_text = models.CharField(max_length=255, null=True, blank=True)
#     value_number = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     value_date = models.DateField(null=True, blank=True)
#     value_file = models.FileField(upload_to='dynamic_field_files/', null=True, blank=True)
#
#     value_image = models.ImageField(upload_to='dynamic_field_images/', null=True, blank=True)
#
#     SELECT_CHOICES = [
#         ('option1', 'Option 1'),
#         ('option2', 'Option 2'),
#         ('option3', 'Option 3'),
#     ]
#     value_select = models.CharField(max_length=20, choices=SELECT_CHOICES, null=True, blank=True)
#
#     @staticmethod
#     def get_dynamic_choices():
#         # Logic to retrieve choices from an external source or the admin panel
#         # For demonstration purposes, let's assume the choices are retrieved from a database
#         dynamic_choices = [
#             ('option1', 'Option 1'),
#             ('option2', 'Option 2'),
#             ('option3', 'Option 3'),
#         ]
#         return dynamic_choices
#
#     # Field with selectable choices
#     selective_field = models.CharField(
#         max_length=20,
#         choices=get_dynamic_choices(),  # Ensure to call the method to get the choices
#         blank=True,
#         null=True
#     )


class Book(models.Model):
    title = models.CharField(blank=True, null=True, max_length=100)

    genre = models.CharField(blank=True, null=True, max_length=100)

    price = models.FloatField(blank=True, null=True)

    quantity = models.IntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    average_rate = models.FloatField(default=0, blank=True, null=True, verbose_name="میانگین امتیاز")

    count_comment = models.IntegerField(default=0, blank=True, null=True, verbose_name="تعداد نظرات")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    # dynamic_fields = GenericRelation(DynamicField, default=None)


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_comment',
                             verbose_name="کاربر")

    created_date = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="تاریخ ایجاد")

    approved = models.BooleanField(default=False, blank=True, null=True, verbose_name="تایید شده")

    text = models.TextField(blank=True, null=True, verbose_name="متن")

    rate = models.PositiveIntegerField(default=5, blank=True, null=True)

    # dynamic_fields = GenericRelation(DynamicField, default=None)

    def update_rate(self):
        rating_average = Comment.objects.filter(book=self.book).aggregate(Avg('rate'), Count('id'))
        Book.objects.filter(id=self.book).update(
            count_comment=rating_average.get('id__count'),
            average_rate=round(rating_average.get('rate__avg'), 1)
        )


# class DynamicForm(models.Model):
#     title = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.title
#
#
# class DynamicFormField(models.Model):
#     FIELD_CHOICES = [
#         ('CharField', 'Text'),
#         ('IntegerField', 'Integer'),
#         ('BooleanField', 'Boolean'),
#         # Add more field types as needed
#     ]
#     value_file = models.FileField(upload_to='dynamic_field_files/', null=True, blank=True)
#     form = models.ForeignKey(DynamicForm, on_delete=models.CASCADE, related_name='fields')
#     field_type = models.CharField(max_length=20, choices=FIELD_CHOICES)
#     label = models.CharField(max_length=100)
#
#     def __str__(self):
#         return f"{self.label} - {self.field_type}"
#
#
# class FormData(models.Model):
#     # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     # object_id = models.PositiveIntegerField()
#     # content_object = GenericForeignKey('content_type', 'object_id')
#     title = models.CharField(max_length=100, default='form')
#     # Add any other fields common to the form data
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Form Data for {self.title}"
#
#
# class FormFieldData(models.Model):
#     form_data = models.ForeignKey(FormData, on_delete=models.CASCADE, related_name='field_data')
#     field = models.ForeignKey(DynamicFormField, on_delete=models.CASCADE)
#     value = models.CharField(max_length=255)  # Adjust the field type based on your needs
#
#     def __str__(self):
#         return f"{self.form_data} - {self.field.label}: {self.value}"