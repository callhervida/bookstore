
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer
from .models import User


class Registration(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()