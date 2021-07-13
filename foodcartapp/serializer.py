from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from foodcartapp.models import Order, OrderElement


class OrderElementsSerializer(ModelSerializer):
    quantity = CharField(source='count')

    class Meta:
        model = OrderElement
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True, source='order_products')

    def validate_products(self, value):
        if not value:
            raise ValidationError('Expects products field to not be empty')
        return value

    def create(self, validated_data):
        order = Order.objects.create(
            address=validated_data.get('address'),
            firstname=validated_data.get('firstname'),
            lastname=validated_data.get('lastname'),
            phonenumber=validated_data.get('phonenumber')
        )

        for serialize_product in validated_data.get('order_products'):
            order.order_product.create(
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
