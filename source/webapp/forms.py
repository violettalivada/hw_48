from django import forms
from .models import DEFAULT_CATEGORY, CATEGORY_CHOICES


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Название')
    description = forms.CharField(max_length=2000, required=True, label='Описание', widget=forms.Textarea)
    category = forms.ChoiceField(required=True, initial=DEFAULT_CATEGORY, choices=CATEGORY_CHOICES, label='Категория')
    amount = forms.IntegerField(label='Остаток', min_value=0, required=True)
    price = forms.DecimalField(label='Цена', max_digits=7, decimal_places=2, required=True, min_value=0)

