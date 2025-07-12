
from django.urls import path
from . import views
from .views_logout import CustomLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('pending-approval/', views.pending_approval_view, name='pending_approval'),
    path('check-approval/', views.check_approval_status, name='check_approval'),
    # Role-based dashboards
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # Doctor views for patients
    path('patients/', views.patient_list_view, name='patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail_view, name='patient_detail'),
    path('patients/<int:patient_id>/documents/<int:document_id>/', views.patient_document_view, name='patient_document'),
    path('ajax/assign-patient/<int:patient_id>/', views.assign_patient_ajax, name='assign_patient_ajax'),
]