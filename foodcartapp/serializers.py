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

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product in products_data:
            price = Product.objects.get(id=product['product'].id).price
            OrderItems.objects.create(order=order, price=price, **product)
        return order
