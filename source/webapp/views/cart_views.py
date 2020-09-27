from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DeleteView, CreateView

from webapp.models import Cart, Product
from webapp.forms import CartAddProductForm, OrderForm


class CartAddProductView(CreateView):
    model = Cart
    form_class = CartAddProductForm

    def post(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        qty = form.cleaned_data.get('qty', 1)

        try:
            cart_product = Cart.objects.get(products=self.product, pk__in=self.get_cart_ids())
            cart_product.qty += qty
            if cart_product.qty <= self.product.amount:
                cart_product.save()
        except Cart.DoesNotExist:
            if qty <= self.product.amount:
                cart_product = Cart.objects.create(products=self.product, qty=qty)
                self.save_to_session(cart_product)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('webapp:index')

    def get_cart_ids(self):
        return self.request.session.get('cart_ids', [])

    def save_to_session(self, cart_product):
        cart_ids = self.request.session.get('cart_ids', [])
        if cart_product.pk not in cart_ids:
            cart_ids.append(cart_product.pk)
        self.request.session['cart_ids'] = cart_ids


class CartView(ListView):
    template_name = 'cart/cart_view.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart.get_with_product().filter(pk__in=self.get_cart_ids())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['cart_total'] = Cart.get_cart_total(ids=self.get_cart_ids())
        context['form'] = OrderForm()
        return context

    def get_cart_ids(self):
        cart_ids = self.request.session.get('cart_ids', [])
        print(cart_ids)
        return self.request.session.get('cart_ids', [])


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.delete_from_session()
        self.object.delete()
        return redirect(success_url)

    def delete_from_session(self):
        cart_ids = self.request.session.get('cart_ids', [])
        cart_ids.remove(self.object.pk)
        self.request.session['cart_ids'] = cart_ids

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CartDeleteOneView(CartDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.qty -= 1
        if self.object.qty < 1:
            self.delete_from_session()
            self.object.delete()
        else:
            self.object.save()
        return redirect(success_url)