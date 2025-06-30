from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Job

class JobListView(ListView):
    model = Job
    context_object_name = 'jobs'
    template_name = 'jobs/list.html'

class JobDetailView(DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'jobs/detail.html'

class JobCreateView(CreateView):
    model = Job
    fields = '__all__'
    template_name = 'jobs/form.html'
    success_url = reverse_lazy('jobs_list')

class JobUpdateView(UpdateView):
    model = Job
    fields = '__all__'
    template_name = 'jobs/form.html'
    success_url = reverse_lazy('jobs_list')

class JobDeleteView(DeleteView):
    model = Job
    template_name = 'jobs/confirm_delete.html'
    success_url = reverse_lazy('jobs_list')
