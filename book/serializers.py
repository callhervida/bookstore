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
        rate = validated_data['rate']
        if not 0 < rate < 5:
            serializers.ValidationError("must be between 0-5")

        rating_average = Comment.objects.filter(book=validated_data['book']).aggregate(Avg('rate'), Count('id'))
        Book.objects.filter(id=validated_data['book']).update(
            count_comment=rating_average.get('id__count'),
            average_rate=round(rating_average.get('rate__avg'), 1)
        )

        return Comment.objects.create(**validated_data)

    def validate(self, data):

        if not data['rate']:
            raise serializers.ValidationError("rate first")
        return data
