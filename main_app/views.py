from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Device


# ---------- Simple pages ----------
def home(request):
    return render(request, "main_app/home.html")


def about(request):
    return render(request, "main_app/about.html")


# ---------- Owner-only Mixin ----------
class OwnerOnlyMixin:
    """
    Restrict updates/deletes to the user who created the object.
    If the model has a `created_by` field and it doesn't match the
    current user, respond with 404.
    """
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(obj, "created_by") and obj.created_by_id and obj.created_by_id != self.request.user.id:
            raise Http404("Not found")
        return obj


# ---------- Device Views ----------
class DeviceListView(ListView):
    model = Device
    template_name = "main_app/chromebooks/index.html"
    context_object_name = "devices"
    paginate_by = 20  # optional: paginates if you add lots of devices

    def get_queryset(self):
        # Show all devices (readable by anyone).
        # If you prefer to show only the current user's devices, uncomment the filter below.
        qs = Device.objects.all().order_by("asset_tag")
        # if self.request.user.is_authenticated:
        #     qs = qs.filter(created_by=self.request.user)
        return qs


class DeviceDetailView(DetailView):
    model = Device
    template_name = "main_app/chromebooks/detail.html"
    context_object_name = "device"


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    fields = ["asset_tag", "serial_number", "manufacturer", "model", "status", "condition", "notes"]
    template_name = "main_app/chromebooks/form.html"
    success_url = reverse_lazy("device-index")

    def form_valid(self, form):
        # Tag the creator for authorization rules & audit
        if hasattr(self.model, "created_by"):
            form.instance.created_by = self.request.user
        messages.success(self.request, "✅ Device created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # helpful labels for the shared form template
        ctx["action_label"] = "Create Device"
        ctx["button_label"] = "Create"
        return ctx


class DeviceUpdateView(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    model = Device
    fields = ["asset_tag", "serial_number", "manufacturer", "model", "status", "condition", "notes"]
    template_name = "main_app/chromebooks/form.html"
    success_url = reverse_lazy("device-index")

    def form_valid(self, form):
        messages.success(self.request, "✏️ Device updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["action_label"] = "Update Device"
        ctx["button_label"] = "Update"
        return ctx


class DeviceDeleteView(LoginRequiredMixin, OwnerOnlyMixin, DeleteView):
    model = Device
    template_name = "main_app/chromebooks/confirm_delete.html"
    success_url = reverse_lazy("device-index")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Device deleted.")
        return super().delete(request, *args, **kwargs)
