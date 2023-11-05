from rest_framework import serializers

from book.models import Book
from book.serializers import GetBookSerializer
from .models import User, AuthorProfile


class AuthorSerializer(serializers.ModelSerializer):
    books = GetBookSerializer(read_only=True)

    def get_books(self, obj):
        return GetBookSerializer(obj.books).data

    class Meta:
        model = AuthorProfile
        fields = '__all__'

    def create(self, validated_data):
        book = validated_data['book']
        obj = super().create(validated_data)
        obj.books = book
        obj.save()
        return obj


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
