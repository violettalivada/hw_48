from django import forms
from .models import Product, Order, Cart

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class CartAddProductForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['qty']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user_name', 'user_phone', 'user_address']