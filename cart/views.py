from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from .models import OrderItem, Order


class AddToCart(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request):

        user = request.user
        book_id = request.data.get('book_id')

        book_obj = Book.objects.filter(id=book_id).first()

        order_item, status = OrderItem.objects.get_or_create(product=book_obj)

        # create order associated with the user
        user_order, status = Order.objects.get_or_create(owner=user, is_ordered=False)
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

    def post(self, request):

        item_id = request.data.get('item_id')

        item_obj = OrderItem.objects.filter(id=item_id)

        if not item_obj:
            return Response(
                {
                    'status': False,
                    'message': 'item object does not exist!',
                    'data': []
                },
                status=200
            )

        item_obj[0].delete()

        return Response(
            {
                'status': True,
                'message': 'Item has been deleted',
                'data': []
            },
            status=200
        )