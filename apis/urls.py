from django.urls import path, include
from .views import UserViewSet, ProductViewSet, OrderViewSet, OrderItemViewset, ShippingViewSet, CustomerViewSet
from .views import MyTokenObtainPairView

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router= routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-item', OrderItemViewset)
router.register(r'shipping', ShippingViewSet)

urlpatterns= [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]