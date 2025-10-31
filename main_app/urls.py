from django.urls import path
from . import views

urlpatterns = [
    # basic pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),

    # Device CRUD
    path("devices/", views.DeviceListView.as_view(), name="device-index"),
    path("devices/create/", views.DeviceCreateView.as_view(), name="device-create"),
    path("devices/<int:pk>/", views.DeviceDetailView.as_view(), name="device-detail"),
    path("devices/<int:pk>/update/", views.DeviceUpdateView.as_view(), name="device-update"),
    path("devices/<int:pk>/delete/", views.DeviceDeleteView.as_view(), name="device-delete"),
]

