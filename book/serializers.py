from rest_framework import serializers
from django.db.models import Count, Avg


from django.contrib.auth.models import User

from .models import Book, Comment


class GetBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    text = serializers.CharField(max_length=100)
    rate = serializers.IntegerField()

    def create(self, validated_data):

        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):

        return super().update(instance, validated_data)

    def validate(self, data):

        if not data['rate']:
            raise serializers.ValidationError("rate first")
        return data
