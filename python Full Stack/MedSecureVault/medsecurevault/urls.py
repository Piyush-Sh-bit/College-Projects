from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def dashboard_redirect(request):
    """Smart redirect to appropriate dashboard based on user role"""
    try:
        if request.user.is_authenticated:
            if hasattr(request.user, 'role'):
                if request.user.role == 'admin':
                    return redirect('accounts:admin_dashboard')
                elif request.user.role == 'doctor':
                    if getattr(request.user, 'is_approved_doctor', False):
                        return redirect('accounts:doctor_dashboard')
                    else:
                        return redirect('accounts:pending_approval')
                else:  # patient
                    return redirect('accounts:patient_dashboard')
            return redirect('accounts:patient_dashboard')
        return redirect('accounts:login')
    except Exception:
        return redirect('accounts:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('documents/', include('documents.urls')),
    path('dashboard/', include('documents.urls')),
    path('', dashboard_redirect),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)