from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from .models import Book
from .serializers import GetBookSerializer, UserSerializer, BookSerializer
from django.contrib.auth.models import User


class Registration(CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()


class NewBook(CreateAPIView):

    serializer_class = GetBookSerializer
    queryset = Book.objects.all()

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GetBook(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = GetBookSerializer


class EditBook(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
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
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'genre', 'author__username']
    filterset_fields = ['genre']
    ordering_fields = ['title', 'genre']
    pagination_class = PaginationNumber





