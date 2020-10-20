from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAdminUser

from api.serrializers import ProductSerializer, OrderSerializer
from webapp.models import Product, Order


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class OrderApi(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'))
        slr = OrderSerializer(order)
        return Response(slr.data)

    def post(self, request, *args, **kwargs):
        slr = OrderSerializer(data=request.data)
        if slr.is_valid():
            order = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return []
        return super().get_permissions()
