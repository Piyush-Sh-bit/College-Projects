from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product

class ProductListView(ListView):
    model = Product
    context_object_name = 'catalog'
    template_name = 'catalog/list.html'

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'catalo'
    template_name = 'catalog/detail.html'

class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'catalog/form.html'
    success_url = reverse_lazy('catalog_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'catalog/form.html'
    success_url = reverse_lazy('catalog_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('catalog_list')
