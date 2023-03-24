from rest_framework import serializers
from mainbox.models import product, customer, order, orderItems, shippingAddress
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # products= serializers.HyperlinkedRelatedField(many= True, view_name='product-detail', read_only= True)
    class Meta:
        model= User
        fields=[
            'id',
            'url',
            'username',
        ]

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    user= serializers.HyperlinkedRelatedField(many= False, view_name='user-detail', read_only= True)
    products= serializers.HyperlinkedRelatedField(many=True, view_name='product-detail', read_only=True)
    class Meta:
        model= customer
        fields= [
            'url',
            'user',
            'name',
            'email',
            'products'
        ]

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner= serializers.HyperlinkedRelatedField(many= False, view_name='user-detail', read_only=True)
    class Meta:
        model= product
        fields= [
            'url',
            'id',
            'name',
            'price',
            'digital',
            'owner'
        ]

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer= serializers.HyperlinkedRelatedField(many= False, view_name='customer-detail', read_only=True)
    class Meta:
        model= order
        fields=[
            'url',
            'customer',
            'date_ordered',
            'complete',
            'transaction_id'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product= serializers.HyperlinkedRelatedField(many= True, view_name='product-detail', read_only= True)
    order= serializers.HyperlinkedRelatedField(many= True, view_name='order-detail', read_only= True)
    class Meta:
        model= orderItems
        fields=[
            'product',
            'order',
            'quantity',
            'date_added'
        ]

class ShippingSerializer(serializers.ModelSerializer):
    customer= serializers.HyperlinkedRelatedField(many= True, view_name='customer-detail', read_only=True)
    order= serializers.HyperlinkedRelatedField(many=True, view_name='order-detail', read_only=True)
    class Meta:
        model= shippingAddress
        fields= [
            'url',
            'customer',
            'order',
            'address',
            'city',
            'state',
            'zipcode',
            'date_added'
        ]


