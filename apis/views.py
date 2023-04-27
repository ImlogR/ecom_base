from rest_framework import viewsets, status, generics
from django.contrib.auth.models import User
from . import serializers
from mainbox.models import product, customer, order, orderItems, shippingAddress
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from mainbox.models import customer


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

# def get_tokens_for_user(user):
#   refresh = RefreshToken.for_user(user)
#   return {
#       'refresh': str(refresh),
#       'access': str(refresh.access_token),
#   }


class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset= User.objects.all()
    serializer_class= serializers.UserSerializer

class UserRegistrationViewSet(viewsets.ViewSet):
    queryset= User.objects.all()
    serializer_class= serializers.UserRegistrationSerializer

    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        new_customer= customer.objects.create(user= user,name= user.username, email= user.email)
        new_customer.save()
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    

class UserLoginViewSet(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class= serializers.UserLoginSerializer
    permission_classes= [AllowAny]

    def list(self, request, *args, **kwargs):
        return Response({"error":"login_required"})
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({'msg': 'Login Success', 'user': user.username}, status=status.HTTP_200_OK)

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