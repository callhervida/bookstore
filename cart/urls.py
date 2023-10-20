from django.urls import path
from .views import AddToCart, DeleteFromCart, ViewCart

urlpatterns = [
    path('add/', AddToCart.as_view()),
    path('delete/', DeleteFromCart.as_view()),
    path('display/', ViewCart.as_view()),

]