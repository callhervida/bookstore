from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.apps import apps
from django.db.models import Count, Avg
from django import forms
import time
from django.utils import timezone
from user.permissions import IsAuthor
from .models import Book, Comment
from .serializers import GetBookSerializer, CommentSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#
# class CreateBooksAPIView(APIView):
#     def get(self, request):
#         start_time = time.time()
#
#         books_data = []
#         for i in range(1000):
#             book_data = {
#                 'title': f'Book {i+1}',
#                 'price': 9.99,  # Set the price as needed
#                 'quantity': 1,  # Set the quantity as needed
#                 # Other fields for the Book model as needed
#             }
#             books_data.append(book_data)
#
#         books_serializer = BookSerializer(data=books_data, many=True)
#         if books_serializer.is_valid():
#             books = books_serializer.save()
#
#             # Create dynamic fields for each book
#             for book in books:
#                 DynamicField.objects.create(
#                     name='pages',
#                     value_number=1000,
#                     content_object=book
#                 )
#             end_time = time.time()
#             query_time = end_time - start_time
#             print(f"Time taken for query: {query_time} seconds")
#             return Response({'message': 'Successfully created 1000 books'}, status=status.HTTP_201_CREATED)
#         return Response(books_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class RetrieveDynamicFieldsAPIView(APIView):
#     def get(self, request):
#         start_time = time.time()
#         dynamic_fields = DynamicField.objects.filter(name='pages', value_number=1000)
#         retrieved_fields = [{'id': field.id, 'name': field.name, 'value_number': field.value_number} for field in
#                             dynamic_fields]
#         end_time = time.time()
#         query_time = end_time - start_time
#         return Response(
#             {'message': f"Time taken for query: {query_time} seconds", 'retrieved_fields': retrieved_fields},
#             status=status.HTTP_200_OK)
#
#
# class UpdateDynamicFieldsAPIView(APIView):
#     def put(self, request, format=None):
#         start_time = time.time()
#         dynamic_fields = DynamicField.objects.filter(name='pages', value_number=1000)
#         dynamic_fields.update(value_number=2000)  # Update value_number to 2000
#         end_time = time.time()
#         update_time = end_time - start_time
#         return Response({'message': f"Time taken for update: {update_time} seconds"}, status=status.HTTP_200_OK)
#
#
# class DeleteDynamicFieldsAPIView(APIView):
#     def delete(self, request, format=None):
#         start_time = time.time()
#         dynamic_fields = DynamicField.objects.filter(name='pages', value_number=1000)
#         dynamic_fields.delete()
#         end_time = time.time()
#         deletion_time = end_time - start_time
#         return Response({'message': f"Time taken for deletion: {deletion_time} seconds"}, status=status.HTTP_200_OK)
#


class NewBook(CreateAPIView):
    serializer_class = GetBookSerializer
    queryset = Book.objects.all()

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save()


class GetBook(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = GetBookSerializer


class EditBook(UpdateAPIView, IsAuthor):
    permission_classes = (IsAuthenticated, IsAuthor,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = GetBookSerializer


class DeleteBook(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = GetBookSerializer


class PaginationNumber(PageNumberPagination):
    page_size = 5


class SearchBook(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = GetBookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'genre']
    filterset_fields = ['genre']
    ordering_fields = ['title', 'genre']
    pagination_class = PaginationNumber


# class CommentAndRate(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request):
#
#         book_id = request.GET.get('book_id')
#
#         p = request.GET.get('page', 1)
#         r = request.GET.get('records_number', 10)
#
#         comment = Comment.objects.filter(book=book_id,
#                                          approved=True).order_by('-created_date')[
#                   int(r) * (int(p) - 1): int(r) * (int(p))]  # show 'r' records in each page order by last records
#
#         if not comment:
#             return Response(
#                 {
#                     'status': False,
#                     'message': 'there is no comment to display',
#                     'data': []
#                 },
#                 status=200
#             )
#
#         comment_serialized = CommentSerializer(comment, many=True)
#
#         response_json = {
#             'status': True,
#             'message': 'successful',
#             'data': comment_serialized.data
#         }
#
#         return Response(response_json, status=200)
#
#     def post(self, request):
#
#         book_id = request.data.get('book_id')
#         book_comment = request.data.get('comment')
#         rate = request.data.get("rate")
#         user = request.user.id
#
#         if not rate:
#             return Response(
#                 {
#                     'status': False,
#                     'message': 'rate first',
#                     'data': []
#                 },
#                 status=200
#             )
#
#         request_json = {
#             'book': book_id,
#             'text': book_comment,
#             'rate': rate,
#             'user': user
#         }
#
#         comment_serialized = CommentSerializer(data=request_json, partial=True)
#         if not comment_serialized.is_valid():
#             return Response(
#                 {
#                     'status': False,
#                     'message': comment_serialized.errors,
#                     'data': ''
#                 },
#                 status=200
#             )
#
#         comment_serialized.save()
#
#         rating_average = Comment.objects.filter(book=book_id).aggregate(Avg('rate'),
#                                                                                                 Count('id'))
#
#         book_obj = Book.objects.filter(id=book_id).first()
#         if not book_obj:
#             return Response(
#                 {
#                     'status': False,
#                     'message': 'book object does not exist!',
#                     'data': []
#                 },
#                 status=200
#             )
#
#         request_json = {
#             'count_comment': rating_average.get('id__count'),
#             "average_rate": round(rating_average.get('rate__avg'), 1)
#         }
#
#         book_serialized = BookSerializer(book_obj, data=request_json, partial=True)
#
#         if not book_serialized.is_valid():
#             return Response(
#                 {
#                     'status': False,
#                     'message': book_serialized.errors,
#                     'data': ''
#                 },
#                 status=200
#             )
#         book_serialized.save()
#
#         return Response(
#             {
#                 'status': True,
#                 'message': 'comment has been added',
#                 'data': []
#             },
#             status=200
#         )


class Comment(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        book_id = self.request.data.get('book_id')
        # book_obj = Book.objects.filter(id=int(book_id)).first()
        return serializer.save(user=self.request.user, book=book_id)


# Dynamic form generator
# def get_dynamic_form(form_id):
#     fields = DynamicFormField.objects.filter(id=form_id)
#     form_fields = {}
#     for field in fields:
#         field_type = forms.CharField
#         if field.field_type == 'number':
#             field_type = forms.IntegerField
#         elif field.field_type == 'email':
#             field_type = forms.EmailField
#
#         form_fields[field.label] = field_type(required=field.required)
#
#     return type('DynamicForm', (forms.Form,), form_fields)
#
#
# class DynamicFormAPIView(APIView):
#     def get(self, request, form_id):
#         # Retrieve the form fields based on the form_id
#         form_fields = DynamicFormField.objects.filter(id=form_id)
#
#         # Create a list to hold form field details
#         fields_data = []
#         for field in form_fields:
#             fields_data.append({
#                 'label': field.label,
#                 'field_type': field.field_type,
#                 'required': field.required,
#             })
#
#         # Create the dynamic form class
#         DynamicForm = get_dynamic_form(form_id)
#
#         # Serialize the form fields data
#         serialized_fields = {
#             'form_fields': fields_data,
#             # Here, you might include additional form metadata if needed
#         }
#
#         return Response(serialized_fields, status=status.HTTP_200_OK)