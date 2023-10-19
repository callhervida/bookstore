from django.urls import path
from .views import AddToCart, DeleteFromCart

urlpatterns = [
    path('add/', AddToCart.as_view()),
    path('delete/', DeleteFromCart.as_view()),

]