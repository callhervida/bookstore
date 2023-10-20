from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Comment
from .serializers import GetBookSerializer, UserSerializer, BookSerializer, CommentSerializer
from django.contrib.auth.models import User


class Registration(CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()


class NewBook(CreateAPIView):

    serializer_class = GetBookSerializer
    queryset = Book.objects.all()

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GetBook(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = GetBookSerializer


class EditBook(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = GetBookSerializer


class DeleteBook(DestroyAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    queryset = Book.objects.all()

    serializer_class = GetBookSerializer


class PaginationNumber(PageNumberPagination):
    page_size = 5


class SearchBook(ListCreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'genre', 'author__username']
    filterset_fields = ['genre']
    ordering_fields = ['title', 'genre']
    pagination_class = PaginationNumber


class StoreComments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        book_id = request.data.get('book_id')
        book_comment = request.data.get('comment')
        rate = request.data.get("rate")
        user = request.user.id

        if not rate:
            return Response(
                {
                    'status': False,
                    'message': 'rate first',
                    'data': []
                },
                status=200
            )

        request_json = {
            'store': book_id,
            'text': book_comment,
            'rate': rate,
            'user': user
        }

        comment_serialized = CommentSerializer(data=request_json, partial=True)
        if not comment_serialized.is_valid():
            return Response(
                {
                    'status': False,
                    'message': comment_serialized.errors,
                    'data': ''
                },
                status=200
            )

        comment_serialized.save()

        # calculate average rating and count of comments of the store
        store_rating_average = Comment.objects.filter(store=book_id, store__status=3).aggregate(Avg('rate'),
                                                                                                Count('id'))

        store_obj = Book.objects.filter(id=book_id, status=3).first()
        if not store_obj:
            return Response(
                {
                    'status': False,
                    'message': 'book object does not exist!',
                    'data': []
                },
                status=200
            )

        request_json = {
            'count_comment': store_rating_average.get('id__count'),
            "average_rate": round(store_rating_average.get('rate__avg'), 1)
        }

        book_serialized = BookSerializer(store_obj, data=request_json, partial=True)

        if not book_serialized.is_valid():
            return Response(
                {
                    'status': False,
                    'message': book_serialized.errors,
                    'data': ''
                },
                status=200
            )
        book_serialized.save()

        return Response(
            {
                'status': True,
                'message': 'comment has been added',
                'data': []
            },
            status=200
        )






