from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Q

from .models import Student, Staff, Device, Checkout


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "main_app/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["students_count"] = Student.objects.filter(created_by=user).count()
        ctx["devices_available"] = Device.objects.filter(
            created_by=user, status="AVAILABLE"
        ).count()
        ctx["devices_out"] = Device.objects.filter(
            created_by=user, status="CHECKED_OUT"
        ).count()
        today = timezone.now().date()
        ctx["due_today"] = Checkout.objects.filter(
            created_by=user, due_back_at=today, returned_at__isnull=True
        )
        ctx["overdue"] = Checkout.objects.filter(
            created_by=user, due_back_at__lt=today, returned_at__isnull=True
        )
        return ctx


# ======================
#  STUDENT VIEWS
# ======================
class StudentList(LoginRequiredMixin, ListView):
    model = Student
    template_name = "main_app/student_list.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(created_by=self.request.user)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(student_id__icontains=q)
            )
        return qs


class StudentDetail(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "main_app/student_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    fields = [
        "first_name",
        "last_name",
        "student_id",
        "grade_level",
        "guardian_name",
        "guardian_phone",
        "guardian_email",
        "active",
    ]
    template_name = "main_app/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = Student
    fields = [
        "first_name",
        "last_name",
        "student_id",
        "grade_level",
        "guardian_name",
        "guardian_phone",
        "guardian_email",
        "active",
    ]
    template_name = "main_app/form.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")
    template_name = "main_app/confirm_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


# ======================
#  DEVICE VIEWS
# ======================
class DeviceList(LoginRequiredMixin, ListView):
    model = Device
    template_name = "main_app/device_list.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(created_by=self.request.user)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(asset_tag__icontains=q)
                | Q(serial_number__icontains=q)
                | Q(model__icontains=q)
            )
        return qs


class DeviceDetail(LoginRequiredMixin, DetailView):
    model = Device
    template_name = "main_app/device_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class DeviceCreate(LoginRequiredMixin, CreateView):
    model = Device
    fields = [
        "asset_tag",
        "serial_number",
        "manufacturer",
        "model",
        "purchase_date",
        "warranty_expires_on",
        "status",
        "condition",
        "notes",
    ]
    template_name = "main_app/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DeviceUpdate(LoginRequiredMixin, UpdateView):
    model = Device
    fields = [
        "asset_tag",
        "serial_number",
        "manufacturer",
        "model",
        "purchase_date",
        "warranty_expires_on",
        "status",
        "condition",
        "notes",
    ]
    template_name = "main_app/form.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class DeviceDelete(LoginRequiredMixin, DeleteView):
    model = Device
    success_url = reverse_lazy("device-list")
    template_name = "main_app/confirm_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


# ======================
#  CHECKOUT VIEWS
# ======================
class CheckoutList(LoginRequiredMixin, ListView):
    model = Checkout
    template_name = "main_app/checkout_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class CheckoutDetail(LoginRequiredMixin, DetailView):
    model = Checkout
    template_name = "main_app/checkout_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class CheckoutCreate(LoginRequiredMixin, CreateView):
    model = Checkout
    fields = [
        "device",
        "student",
        "staff",
        "due_back_at",
        "condition_out",
        "comments",
    ]
    template_name = "main_app/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        resp = super().form_valid(form)
        device = self.object.device
        device.status = "CHECKED_OUT"
        device.save(update_fields=["status"])
        return resp


class CheckoutUpdate(LoginRequiredMixin, UpdateView):
    model = Checkout
    fields = [
        "device",
        "student",
        "staff",
        "due_back_at",
        "returned_at",
        "condition_out",
        "condition_in",
        "comments",
    ]
    template_name = "main_app/form.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def form_valid(self, form):
        was_returned = (
            form.instance.returned_at is None
            and form.cleaned_data.get("returned_at") is not None
        )
        resp = super().form_valid(form)
        if was_returned:
            device = self.object.device
            device.status = "AVAILABLE"
            device.save(update_fields=["status"])
        return resp


class CheckoutDelete(LoginRequiredMixin, DeleteView):
    model = Checkout
    success_url = reverse_lazy("checkout-list")
    template_name = "main_app/confirm_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)
