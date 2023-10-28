from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.views import Registration, AuthorRegistration


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', Registration.as_view()),
    path('author/', AuthorRegistration.as_view()),
]