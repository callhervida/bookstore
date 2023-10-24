from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.views import Registration


url_pattern = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', Registration.as_view()),
]