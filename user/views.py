
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer, AuthorSerializer
from .models import User


class Registration(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()


# class AuthorRegistration(CreateAPIView):
#     serializer_class = AuthorSerializer
#     queryset = Author.objects.all()
#
#     def perform_create(self, serializer):
#         return serializer.save()
