from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Book
from .serializers import BookSerializer, UserSerializer
from django.contrib.auth.models import User


class Registration(CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()


class NewBook(CreateAPIView):

    serializer_class = BookSerializer
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

    serializer_class = BookSerializer


class EditBook(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = BookSerializer


class DeleteBook(DestroyAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = BookSerializer


