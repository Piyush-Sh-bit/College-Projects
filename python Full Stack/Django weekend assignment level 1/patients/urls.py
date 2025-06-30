from django.urls import path
from .views import PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView, PatientDeleteView

urlpatterns = [
    path('', PatientListView.as_view(), name='patients_list'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patients_detail'),
    path('add/', PatientCreateView.as_view(), name='patients_add'),
    path('<int:pk>/edit/', PatientUpdateView.as_view(), name='patients_edit'),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='patients_delete'),
]
