from rest_framework import serializers
from .models import Cart, CartItem, UserOrder


class CartSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=CartItem.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'items']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        items = validated_data['items']
        cart, created = Cart.objects.get_or_create(user=user, items=items)
        if not created:
            cart.save()
        return cart


class UserOrderSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=CartItem.objects.all())

    class Meta:
        model = UserOrder
        fields = ('id', 'owner', 'items', 'ordered_on')

