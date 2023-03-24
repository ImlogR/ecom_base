from rest_framework import viewsets
from django.contrib.auth.models import User
from . import serializers
from mainbox.models import product, customer, order, orderItems, shippingAddress
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


###simple jwt#####
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


#########overriding jwt's serializers and viewsets########

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class= MyTokenObtainPairSerializer




class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset= User.objects.all()
    serializer_class= serializers.UserSerializer

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset= customer.objects.all()
    serializer_class= serializers.CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset= product.objects.all()
    serializer_class= serializers.ProductSerializer

    permission_classes= [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(owner= self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset= order.objects.all()
    serializer_class= serializers.OrderSerializer

    permission_classes=[
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    def perform_create(self, serializer):
        serializer.save(customer= self.request.user)

class OrderItemViewset(viewsets.ModelViewSet):
    queryset= orderItems.objects.all()
    serializer_class= serializers.OrderItemSerializer

    permission_classes=[
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    def perform_create(self, serializer):
        serializer.save(product= product, order= order )

class ShippingViewSet(viewsets.ModelViewSet):
    queryset= shippingAddress.objects.all()
    serializer_class= serializers.ShippingSerializer

    permission_classes=[
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    def perform_create(self, serializer):
        serializer.save(customer= self.request.user, order= order)




















# @api_view(['GET'])
# def get_routes(request):
#     routes= [
#         '/api/token',
#         '/api/token/refresh',
#     ]
#     return Response(routes)

# @api_view(['GET', 'POST'])
# def product_api(request):
#     if request.method == 'GET':
#         products= product.objects.all()
#         serializer= productSerializer(products, many= True)
#         return Response(serializer.data)
#     elif request.method== 'POST':
#         data= request.data
#         serializer= productSerializer(data= data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_details_api(requset, id):
#     try:
#         products= product.objects.get(id= id)
#     except product.DoesNotExist:
#         return HttpResponse(status= 404)
    
#     if requset.method== 'GET':
#         serializer= productSerializer(products)
#         return Response(serializer.data)

#     elif requset.method== 'PUT':
#         data= requset.data
#         serializer= productSerializer(products, data=data)
#         if serializer.is_valid():
#             serializer.save();
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status= 400)
    
#     else:
#         products.delete()
#         return HttpResponse(status= 204)