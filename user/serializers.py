from rest_framework import serializers


from .models import User, Author, AuthorProfile


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        user = self.context['request'].user
        for authors_data in authors_data:
            AuthorProfile.objects.create(user=user, **authors_data)
        return user




