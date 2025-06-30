from django.urls import path
from .views import JobListView, JobDetailView, JobCreateView, JobUpdateView, JobDeleteView

urlpatterns = [
    path('', JobListView.as_view(), name='jobs_list'),
    path('<int:pk>/', JobDetailView.as_view(), name='jobs_detail'),
    path('add/', JobCreateView.as_view(), name='jobs_add'),
    path('<int:pk>/edit/', JobUpdateView.as_view(), name='jobs_edit'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='jobs_delete'),
]
