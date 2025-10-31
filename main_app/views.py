from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Device

def home(request):
    return render(request, 'main_app/home.html')

def about(request):
    return render(request, 'main_app/about.html')

class DeviceListView(ListView):
    model = Device
    template_name = 'main_app/chromebooks/index.html'

class DeviceDetailView(DetailView):
    model = Device
    template_name = 'main_app/chromebooks/detail.html'

class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    fields = ['asset_tag', 'serial_number', 'manufacturer', 'model', 'status', 'condition']
    template_name = 'main_app/chromebooks/form.html'
    success_url = reverse_lazy('device-index')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_label'] = 'Create Device'
        ctx['button_label'] = 'Create'
        return ctx

    def form_valid(self, form):
        # set owner if model has created_by (we add this in step 4)
        if hasattr(self.model, "created_by"):
            form.instance.created_by = self.request.user
        return super().form_valid(form)

class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    fields = ['asset_tag', 'serial_number', 'manufacturer', 'model', 'status', 'condition']
    template_name = 'main_app/chromebooks/form.html'
    success_url = reverse_lazy('device-index')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_label'] = 'Update Device'
        ctx['button_label'] = 'Update'
        return ctx

class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    template_name = 'main_app/chromebooks/confirm_delete.html'
    success_url = reverse_lazy('device-index')