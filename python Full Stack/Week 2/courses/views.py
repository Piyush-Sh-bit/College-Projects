from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course

class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'courses/list.html'

class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/detail.html'

class CourseCreateView(CreateView):
    model = Course
    fields = '__all__'
    template_name = 'courses/form.html'
    success_url = reverse_lazy('courses_list')

class CourseUpdateView(UpdateView):
    model = Course
    fields = '__all__'
    template_name = 'courses/form.html'
    success_url = reverse_lazy('courses_list')

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/confirm_delete.html'
    success_url = reverse_lazy('courses_list')
