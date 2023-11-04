from rest_framework import serializers


from .models import User, AuthorProfile


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        role = validated_data['role']
        # book = validated_data['book']
        print(validated_data)
        if role == 'AUTHOR':
            # if not book:
                # return 'book is required'

            author = AuthorProfile.objects.create(user=user, is_active=True)
            # author.book.add(book)

        return user
