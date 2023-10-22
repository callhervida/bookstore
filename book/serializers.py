from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Book, Comment, Author


class GetBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('author', )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        user = User.objects.create(**validated_data)
        for authors_data in authors_data:
            Author.objects.create(user=user, **authors_data)
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'