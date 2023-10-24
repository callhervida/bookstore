from django.urls import path

from .views import NewBook, GetBook, EditBook, DeleteBook, SearchBook, Comment

urlpatterns = [

    path('new-book/', NewBook.as_view()),
    path('get-book/<int:id>/', GetBook.as_view()),
    path('edit-book/<int:id>/', EditBook.as_view()),
    path('delete-book/<int:id>/', DeleteBook.as_view()),
    path('search/', SearchBook.as_view()),
    path('comment/', Comment.as_view()),
]

