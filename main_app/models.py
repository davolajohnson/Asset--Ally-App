from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


# -----------------------
# Core People
# -----------------------
class Student(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    student_id = models.CharField(max_length=40, unique=True)
    grade_level = models.CharField(max_length=10, blank=True)   # e.g., "6", "7", "8"
    homeroom = models.CharField(max_length=40, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=40, blank=True)
    guardian_email = models.EmailField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_id})"


class Staff(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=40, blank=True)  # Operations, IT, Teacher, etc.
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


# -----------------------
# Devices
# -----------------------
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="GOOD")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["asset_tag"]

    def __str__(self):
        return f"{self.asset_tag} — {self.model or 'Device'}"


# -----------------------
# Checkouts (loan history)
# -----------------------
class Checkout(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="checkouts")
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.PROTECT, related_name="checkouts")
    staff = models.ForeignKey(Staff, null=True, blank=True, on_delete=models.PROTECT, related_name="checkouts")

    checked_out_at = models.DateTimeField(auto_now_add=True)
    due_back_at = models.DateField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    condition_out = models.CharField(max_length=10, blank=True)  # NEW|GOOD|FAIR|POOR
    condition_in = models.CharField(max_length=10, blank=True)   # on return
    comments = models.TextField(blank=True)

    class Meta:
        # DB-level backstop: only one open checkout per device
        constraints = [
            models.UniqueConstraint(
                fields=["device"],
                name="uniq_device_open_checkout",
                condition=Q(returned_at__isnull=True),
            )
        ]
        ordering = ["-checked_out_at"]

    def clean(self):
        """
        App-level guard to prevent a second open (returned_at IS NULL) checkout for the same device.
        Triggers a form error in Admin/Forms and blocks programmatic saves too (via save()).
        """
        # if this row is marked returned, it's not "open" — nothing to check
        if self.returned_at is not None:
            return

        # there must be EITHER a student OR a staff member
        if not self.student and not self.staff:
            raise ValidationError({"student": "Select a Student or Staff for this checkout."})

        # find other open checkouts for this device
        qs = Checkout.objects.filter(device=self.device, returned_at__isnull=True)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({"device": "This device already has an open checkout. Return it first."})

    def save(self, *args, **kwargs):
        # Ensure validation always runs (Admin forms call clean, but direct saves may not)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        who = self.student or self.staff
        return f"{self.device.asset_tag} → {who} @ {self.checked_out_at:%Y-%m-%d %H:%M}"
