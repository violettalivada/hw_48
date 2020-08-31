from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from webapp.models import Cart, Product
from webapp.forms import CartAddProductForm


class CartAddProductView(View):
    def post(self, request, *args, **kwargs):
        form = CartAddProductForm(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        qty = form.cleaned_data['qty']
        cart = Cart.objects.filter(product=product).first()
        if cart:
            cart.qty += qty
            if product.amount > cart.qty:
                cart.save()
        else:
            if product.amount >= qty:
                cart = Cart.objects.create(products=product, qty=qty)
                cart.save()
            else:
                redirect('index')
        return redirect('index')



