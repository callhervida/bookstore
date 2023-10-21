from django.urls import path
from .views import AddToCart, DeleteFromCart, ViewCart, OrderCreateAPIView, UserOrderListAPIView

urlpatterns = [
    path('add/', AddToCart.as_view()),
    path('delete/', DeleteFromCart.as_view()),
    path('display/', ViewCart.as_view()),
    path('place-order/', OrderCreateAPIView.as_view(), name='place_order'),
    path('my-orders/', UserOrderListAPIView.as_view(), name='my_orders'),

]