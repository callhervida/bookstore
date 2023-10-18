from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import NewBook, GetBook, EditBook, DeleteBook, Registration

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', Registration.as_view()),
    path('new-book/', NewBook.as_view()),
    path('get-book/<int:id>/', GetBook.as_view()),
    path('edit-book/<int:id>/', EditBook.as_view()),
    path('delete-book/<int:id>/', DeleteBook.as_view()),
]
