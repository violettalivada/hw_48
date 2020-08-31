from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView

from webapp.models import Cart, Product
from webapp.forms import CartAddProductForm, OrderForm


class CartAddProductView(View):
    def post(self, request, *args, **kwargs):
        form = CartAddProductForm(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        qty = form.cleaned_data['qty']
        cart = Cart.objects.filter(products=product).first()
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


class CartView(ListView):
    template_name = 'cart/cart_view.html'
    context_object_name = 'products'
    model = Cart
    paginate_by = 5
    paginate_orphans = 0

    def get_queryset(self):
        data = Cart.objects.all()
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm
        data = Cart.objects.all()
        total = 0
        for i in data:
            total += i.qty * i.products.price
        context['total'] = total
        return context
