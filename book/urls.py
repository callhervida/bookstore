from django.urls import path

from .views import NewBook, GetBook, EditBook, DeleteBook, SearchBook, Comment
from graphene_django.views import GraphQLView
from .schema import schema


urlpatterns = [

    path('new-book/', NewBook.as_view()),
    path('get-book/<int:id>/', GetBook.as_view()),
    path('edit-book/<int:id>/', EditBook.as_view()),
    path('delete-book/<int:id>/', DeleteBook.as_view()),
    path('search/', SearchBook.as_view()),
    path('comment/', Comment.as_view()),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    # path('api/dynamic_fields/create_books/', CreateBooksAPIView.as_view(), name='create_books_api'),
    # path('api/dynamic_fields/retrieve/', RetrieveDynamicFieldsAPIView.as_view(), name='retrieve_dynamic_fields'),
    # path('api/dynamic_fields/update/', UpdateDynamicFieldsAPIView.as_view(), name='update_dynamic_fields'),
    # path('api/dynamic_fields/delete/', DeleteDynamicFieldsAPIView.as_view(), name='delete_dynamic_fields'),

]

