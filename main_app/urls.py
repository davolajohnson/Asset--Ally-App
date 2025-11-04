from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),

    # Students
    path("students/", views.StudentList.as_view(), name="student-list"),
    path("students/create/", views.StudentCreate.as_view(), name="student-create"),
    path("students/<int:pk>/", views.StudentDetail.as_view(), name="student-detail"),
    path("students/<int:pk>/update/", views.StudentUpdate.as_view(), name="student-update"),
    path("students/<int:pk>/delete/", views.StudentDelete.as_view(), name="student-delete"),

    # Devices
    path("devices/", views.DeviceList.as_view(), name="device-list"),
    path("devices/create/", views.DeviceCreate.as_view(), name="device-create"),
    path("devices/<int:pk>/", views.DeviceDetail.as_view(), name="device-detail"),
    path("devices/<int:pk>/update/", views.DeviceUpdate.as_view(), name="device-update"),
    path("devices/<int:pk>/delete/", views.DeviceDelete.as_view(), name="device-delete"),

    # Checkouts
    path("checkouts/", views.CheckoutList.as_view(), name="checkout-list"),
    path("checkouts/create/", views.CheckoutCreate.as_view(), name="checkout-create"),
    path("checkouts/<int:pk>/", views.CheckoutDetail.as_view(), name="checkout-detail"),
    path("checkouts/<int:pk>/update/", views.CheckoutUpdate.as_view(), name="checkout-update"),
    path("checkouts/<int:pk>/delete/", views.CheckoutDelete.as_view(), name="checkout-delete"),
]


