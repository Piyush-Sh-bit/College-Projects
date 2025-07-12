from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Patient

class PatientListView(ListView):
    model = Patient
    context_object_name = 'patients'
    template_name = 'patients/list.html'

class PatientDetailView(DetailView):
    model = Patient
    context_object_name = 'patient'
    template_name = 'patients/detail.html'

class PatientCreateView(CreateView):
    model = Patient
    fields = '__all__'
    template_name = 'patients/form.html'
    success_url = reverse_lazy('patients_list')

class PatientUpdateView(UpdateView):
    model = Patient
    fields = '__all__'
    template_name = 'patients/form.html'
    success_url = reverse_lazy('patients_list')

class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'patients/confirm_delete.html'
    success_url = reverse_lazy('patients_list')
