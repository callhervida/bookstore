import graphene
from graphene_django import DjangoObjectType

from user.models import User
from .models import Book


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class BooksType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"


class Query(graphene.ObjectType):

    books = graphene.List(BooksType)

    def resolve_books(self, info):
        return Book.objects.all()


class BookMutation(graphene.Mutation):

    class Arguments:
        title = graphene.String()
        genre = graphene.String()

    book = graphene.List(BooksType)

    @classmethod
    def mutate(cls, self, info, title, genre):
        book = Book.objects.get_or_create(title=title, genre=genre)
        return BookMutation(book=book)


class Mutation(graphene.ObjectType):
    add_book = BookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)