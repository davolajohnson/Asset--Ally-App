from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("asset_tag", "serial_number", "model", "status", "condition")
    list_filter = ("status", "condition")
    search_fields = ("asset_tag", "serial_number", "model", "manufacturer")

