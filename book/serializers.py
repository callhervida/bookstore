from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Book, Comment


class GetBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('author', )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'