from django.urls import path
from .views import CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    path('', CourseListView.as_view(), name='courses_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='courses_detail'),
    path('add/', CourseCreateView.as_view(), name='courses_add'),
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='courses_edit'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='courses_delete'),
]
