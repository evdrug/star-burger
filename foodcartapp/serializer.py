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
    products = OrderElementsSerializer(many=True, allow_empty=False, source='elements')

    def create(self, validated_data):
        order = Order.objects.create(
            address=validated_data['address'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber']
        )

        for serialize_product in validated_data['elements']:
            order.elements.create(
                product=serialize_product['product'],
                count=serialize_product['count'],
                order=order,
                price=serialize_product['product'].price
            )
        return order

    class Meta:
        model = Order
        fields = ['address', 'firstname', 'lastname', 'phonenumber',
                  'products']
