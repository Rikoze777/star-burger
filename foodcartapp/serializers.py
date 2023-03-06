from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItems, Product


class OrderitemsSerializer(ModelSerializer):
    product = Product()

    class Meta:
        model = OrderItems
        fields = ['quantity', 'product']


class OrderSerializer(ModelSerializer):
    products = OrderitemsSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = [
            'address',
            'firstname',
            'lastname',
            'phonenumber',
            'products'
        ]