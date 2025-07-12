from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', ProductListView.as_view(), name='catalog_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='catalog_detail'),
    path('add/', ProductCreateView.as_view(), name='catalog_add'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='catalog_edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='catalog_delete'),
]
