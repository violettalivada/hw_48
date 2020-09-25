from django.urls import reverse
from django.views.generic import CreateView

from webapp.forms import OrderForm
from webapp.models import *


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        name = form.cleaned_data['user_name']
        phone = form.cleaned_data['user_phone']
        address = form.cleaned_data['user_address']
        order = Order.objects.create(user_name=name, user_phone=phone, user_address=address)
        cart = Cart.objects.all()
        for i in cart:
            product = Product.objects.get(pk=i.products.pk)
            OrderProduct.objects.create(product=i.products,
                                        order=order,
                                        qty=i.qty)
            product.amount = product.amount-i.qty
            product.save()
        cart.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:index')