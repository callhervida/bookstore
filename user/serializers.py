from rest_framework import serializers
# from rest_framework.authtoken.admin import User


from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


# class AuthorSerializer(serializers.ModelSerializer):
#     user = UserSerializer(many=True)
#
#     class Meta:
#         model = User
#         fields = '__all__'


