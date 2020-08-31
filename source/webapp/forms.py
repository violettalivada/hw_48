from django import forms
from .models import Product


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class CartAddProductForm(forms.Form):
    qty = forms.IntegerField(min_value=0, required=True, label="Количество",
                             widget=forms.NumberInput(attrs={'class': 'form-control  mt-3 mr-sm-2'}))
