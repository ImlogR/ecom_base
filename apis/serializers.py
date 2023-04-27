from rest_framework import serializers
from mainbox.models import product, customer, order, orderItems, shippingAddress
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    # products= serializers.HyperlinkedRelatedField(many= True, view_name='product-detail', read_only= True)
    class Meta:
        model= User
        fields=[
            'id',
            'url',
            'username',
        ]
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style={'input_type': 'password'}, write_only=True, required= True)

    class Meta:
        model= User
        fields= ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match!")
        return data
    
    def create(self, validated_data):
        user= User.objects.create(
            username= validated_data['username'],
            email= validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid username/password")
        attrs['user'] = user
        return attrs
    
    def create(self, validated_data):
        return validated_data['user']


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
    product= serializers.HyperlinkedRelatedField(many= False, view_name='product-detail', read_only= True)
    order= serializers.HyperlinkedRelatedField(many= False, view_name='order-detail', read_only= True)
    class Meta:
        model= orderItems
        fields=[
            'product',
            'order',
            'quantity',
            'date_added'
        ]

class ShippingSerializer(serializers.ModelSerializer):
    customer= serializers.HyperlinkedRelatedField(many= False, view_name='customer-detail', read_only=True)
    order= serializers.HyperlinkedRelatedField(many=False, view_name='order-detail', read_only=True)
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