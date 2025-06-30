from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('courses/', include('courses.urls')),
    path('jobs/', include('jobs.urls')),
    path('patients/', include('patients.urls')),
]
