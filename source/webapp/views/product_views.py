from django.db.models import Q
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse, reverse_lazy

from webapp.models import Product
from webapp.forms import ProductForm, CartAddProductForm, SimpleSearchForm


class IndexView(ListView):
    model = Product
    template_name = 'products/index.html'
    ordering = ['category', 'name']
    form_class = SimpleSearchForm
    paginate_by = 5
    context_object_name = 'products'

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        data = Product.objects.all()
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(name__icontains=search)).order_by('name')
        if not self.request.GET.get('is_admin', None):
            data = Product.objects.all().filter(amount__gt=0)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddProductForm
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'products/product_view.html'

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddProductForm
        return context


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

