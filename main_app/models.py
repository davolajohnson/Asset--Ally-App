from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q


# ======================
#  STUDENT MODEL
# ======================
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True)
    grade_level = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    guardian_email = models.EmailField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Grade {self.grade_level})"


# ======================
#  STAFF MODEL
# ======================
class Staff(models.Model):
    ROLE_CHOICES = [
        ("Operations", "Operations"),
        ("IT", "IT"),
        ("Teacher", "Teacher"),
        ("Admin", "Admin"),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


# ======================
#  DEVICE MODEL
# ======================
class Device(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("CHECKED_OUT", "Checked Out"),
        ("REPAIR", "Repair"),
        ("LOST", "Lost"),
        ("RETIRED", "Retired"),
    ]

    CONDITION_CHOICES = [
        ("NEW", "New"),
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("POOR", "Poor"),
    ]

    asset_tag = models.CharField(max_length=40, unique=True)
    serial_number = models.CharField(max_length=60, unique=True)
    manufacturer = models.CharField(max_length=60, blank=True)
    model = models.CharField(max_length=80, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expires_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="GOOD")
    notes = models.TextField(blank=True)

    # GA Requirement: Link to User who created the record
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="devices"
    )

    def __str__(self):
        return f"{self.asset_tag} — {self.model or 'Device'}"

    class Meta:
        ordering = ["asset_tag"]


# ======================
#  CHECKOUT MODEL
# ======================
class Checkout(models.Model):
    CONDITION_CHOICES = [
        ("NEW", "New"),
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("POOR", "Poor"),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="checkouts")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name="checkouts")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, related_name="checkouts")

    checked_out_at = models.DateTimeField(auto_now_add=True)
    due_back_at = models.DateField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    condition_out = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    condition_in = models.CharField(max_length=10, choices=CONDITION_CHOICES, null=True, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["device"],
                condition=Q(returned_at__isnull=True),
                name="unique_open_checkout_per_device"
            )
        ]
        ordering = ["-checked_out_at"]

    def clean(self):
        # Prevent multiple open checkouts for same device
        if not self.returned_at:
            open_checkouts = Checkout.objects.filter(device=self.device, returned_at__isnull=True)
            if self.pk:
                open_checkouts = open_checkouts.exclude(pk=self.pk)
            if open_checkouts.exists():
                raise ValidationError(f"{self.device} is already checked out.")

    def save(self, *args, **kwargs):
        self.full_clean()  # run validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        borrower = self.student or self.staff
        return f"{self.device.asset_tag} → {borrower} ({'Returned' if self.returned_at else 'Out'})"