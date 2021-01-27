from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from foodcartapp.models import Order, OrderElements, Product


class OrderElementsSerializer(ModelSerializer):
    quantity = CharField(source='count')

    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True)

    def create(self, validated_data):
        if not validated_data.get('products'):
            raise ValidationError('Expects products field to not be empty')
        order = Order.objects.create(
            address=validated_data.get('address'),
            firstname=validated_data.get('firstname'),
            lastname=validated_data.get('lastname'),
            phonenumber=validated_data.get('phonenumber')
        )
        for serialize_product in validated_data.get('products', []):
            order.products.create(
                product=serialize_product.get('product'),
                count=serialize_product.get('count'),
                order=order,
                price=serialize_product.get('product').price
            )
        return order

    class Meta:
        model = Order
        fields = ['address', 'firstname', 'lastname', 'phonenumber',
                  'products']
