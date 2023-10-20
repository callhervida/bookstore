from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from .models import CartItem, Cart


class AddToCart(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):

        user = request.user
        book_id = request.data.get('book_id')

        book_obj = Book.objects.filter(id=book_id).first()

        order_item, status = CartItem.objects.get_or_create(product=book_obj)

        # create order associated with the user
        user_order, status = Cart.objects.get_or_create(owner=user, is_ordered=False)
        user_order.items.add(order_item)
        if status:
            user_order.save()

        return Response(
            {
                'status': True,
                'message': 'Item added to cart',
                'data': []
            },
            status=200
        )


class DeleteFromCart(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):

        item_id = request.data.get('item_id')

        item_obj = CartItem.objects.filter(id=item_id).first()

        if not item_obj:
            return Response(
                {
                    'status': False,
                    'message': 'item object does not exist!',
                    'data': []
                },
                status=200
            )

        item_obj.delete()

        item_obj = CartItem.objects.all()

        if not item_obj:
            user_id = request.user.id
            cart_obj = Cart.objects.filter(owner=user_id).first()
            cart_obj.delete()

        return Response(
            {
                'status': True,
                'message': 'Item has been deleted',
                'data': []
            },
            status=200
        )


class ViewCart(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get(self, request):

        user_id = request.user.id

        cart_obj = Cart.objects.filter(owner=user_id).first()

        if not cart_obj:
            return Response(
                {
                    'status': False,
                    'message': 'cart object does not exist!',
                    'data': []
                },
                status=200
            )

        cart_items = Cart.get_cart_items(cart_obj)

        return Response(
            {
                'status': True,
                'message': 'Item has been deleted',
                'data': cart_items
            },
            status=200
        )