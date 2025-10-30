from django.contrib import admin
from .models import Device, Student, Staff, Checkout

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "last_name", "first_name", "grade_level", "homeroom", "active")
    list_filter = ("grade_level", "homeroom", "active")
    search_fields = ("student_id", "last_name", "first_name", "guardian_name", "guardian_email")

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email", "role", "active")
    list_filter = ("role", "active")
    search_fields = ("last_name", "first_name", "email")

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("asset_tag", "serial_number", "model", "status", "condition")
    list_filter = ("status", "condition")
    search_fields = ("asset_tag", "serial_number", "model", "manufacturer")

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ("device", "student", "staff", "checked_out_at", "due_back_at", "returned_at")
    list_filter = ("due_back_at", "returned_at")
    search_fields = (
        "device__asset_tag",
        "device__serial_number",
        "student__student_id",
        "student__last_name",
        "staff__last_name",
    )
