from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('author', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
