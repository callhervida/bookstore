from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import NewBook, GetBook

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('new-book/', NewBook.as_view()),
    path('get-book/<pk>', GetBook.as_view()),
]
