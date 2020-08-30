from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from .base_views import SearchView
from webapp.models import Product
from webapp.forms import ProductForm


class IndexView(SearchView):
    model = Product
    template_name = 'products/index.html'
    ordering = ['category', 'name']
    search_fields = ['name__icontains']
    paginate_by = 5
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)


class ProductView(DetailView):
    model = Product
    template_name = 'products/product_view.html'

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)

