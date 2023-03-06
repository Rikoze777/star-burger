from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.templatetags.static import static
from .models import Product, Order, OrderItems
from rest_framework.decorators import api_view
from .serializers import OrderSerializer


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


# def check_order(order, phonenumber):
#     keys = ('address', 'firstname', 'lastname', 'phonenumber')
#     missing_keys = []
#     errors = []
#     products = order.get('products')
#     if not products or not isinstance(products, list):
#         content = {'error': 'products key not presented or not list'}
#         errors.append(content)
#     for key in keys:
#         order_key = order.get(key)
#         if not order_key or not isinstance(order_key, str):
#             missing_keys.append(order_key)
#     if not phonenumbers.is_valid_number(phonenumber):
#         phone_error = {
#             'error': f'Such phonenumber={phonenumber} does not exist'
#         }
#     valid_phonenumber = phonenumbers.format_number(
#         phonenumber,
#         phonenumbers.PhoneNumberFormat.E164,
#     )
#     if missing_keys:
#         miss_content = {'error': f'The keys {missing_keys} not specified or not str'}
#         errors.append(miss_content)
#     return valid_phonenumber, phone_error, errors


@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order = Order.objects.create(
        address=serializer.validated_data['address'],
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        phonenumber=serializer.validated_data['phonenumber'],
    )
    all_products = Product.objects.prefetch_related()
    for product in serializer.validated_data['products']:
        OrderItems.objects.create(
            order=order,
            product=all_products.get(id=product.get('product').id),
            quantity=product.get('quantity'),
        )
    serializer = OrderSerializer(order)
    return Response(serializer.data)
