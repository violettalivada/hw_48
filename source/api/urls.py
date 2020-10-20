from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet, OrderApi

app_name = 'api'

router = DefaultRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('order/<int:pk>/', OrderApi.as_view(), name='order_api'),
]
