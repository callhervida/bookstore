from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import NewBook

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('new-book/', NewBook.as_view()),
]
