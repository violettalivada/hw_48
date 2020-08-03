from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import *
from django.http import HttpResponseNotAllowed
from webapp.forms import ProductForm


def index_view(request):
    is_admin = request.GET.get('is_admin', None)
    if is_admin:
        data = Product.objects.all()
    else:
        data = Product.objects.order_by('name', 'category').exclude(amount=0)
    return render(request, 'index.html', context={'products': data})


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_view.html', context)


def product_create_view(request):
    if request.method == "GET":
        form = ProductForm()
        return render(request, 'product_create.html', context={'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                price=form.cleaned_data['price'])
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_create.html', context={'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'amount': product.amount,
            'price': product.price
        })
        return render(request, 'product_update.html', context={'form': form, 'product': product})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.amount = form.cleaned_data['amount']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_update.html', context={'product': product, 'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'product_delete.html', context={'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


