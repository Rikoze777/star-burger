from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Order, OrderItems, Product


class OrderitemsSerializer(ModelSerializer):
    product = Product()

    class Meta:
        model = OrderItems
        fields = ['quantity', 'product']


class OrderSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    products = OrderitemsSerializer(many=True, allow_empty=False,
                                    write_only=True,)

    def create(self, validated_data):
        return Order(**validated_data)

    class Meta:
        model = Order
        fields = [
            'id',
            'address',
            'firstname',
            'lastname',
            'phonenumber',
            'products',
        ]
