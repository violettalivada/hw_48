from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from webapp.forms import OrderForm
from webapp.models import *


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        order = self.object
        cart_products = Cart.objects.all()
        products = []
        order_products = []
        for item in cart_products:
            product = item.products
            qty = item.qty
            product.amount -= qty
            products.append(product)
            order_product = OrderProduct(order=order, product=product, qty=qty)
            order_products.append(order_product)
        OrderProduct.objects.bulk_create(order_products)
        Product.objects.bulk_update(products, ('amount',))
        cart_products.delete()
        return response

    def form_invalid(self, form):
        return redirect('webapp:cart_view')