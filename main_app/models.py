from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.urls import reverse


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

    # Link to user who created this student
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="students",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Grade {self.grade_level})"

    def get_absolute_url(self):
        # After creating/updating a student, go to its detail page
        return reverse("student-detail", args=[self.pk])


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

    # Optional link to user who created this staff record
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="staff_members",
    )

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

    asset_tag = models.CharField(max_length=40, unique=True, db_index=True)
    serial_number = models.CharField(max_length=60, unique=True, db_index=True)
    manufacturer = models.CharField(max_length=60, blank=True)
    model = models.CharField(max_length=80, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expires_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="GOOD")
    notes = models.TextField(blank=True)

    # Link to User who created the record (authorization / ownership)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="devices",
    )

    class Meta:
        ordering = ["asset_tag"]

    def __str__(self):
        return f"{self.asset_tag} — {self.model or 'Device'}"

    def get_absolute_url(self):
        return reverse("device-detail", args=[self.pk])


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
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=True, related_name="checkouts"
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, null=True, blank=True, related_name="checkouts"
    )

    checked_out_at = models.DateTimeField(auto_now_add=True)
    due_back_at = models.DateField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    condition_out = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    condition_in = models.CharField(max_length=10, choices=CONDITION_CHOICES, null=True, blank=True)
    comments = models.TextField(blank=True)

    # Link to user who created this checkout
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="checkouts",
    )

    class Meta:
        # Postgres partial unique index: only one open checkout per device
        constraints = [
            models.UniqueConstraint(
                fields=["device"],
                condition=Q(returned_at__isnull=True),
                name="unique_open_checkout_per_device",
            )
        ]
        ordering = ["-checked_out_at"]

    @property
    def borrower(self):
        return self.student or self.staff

    def clean(self):
        # (1) Exactly one borrower: either a student OR a staff member
        if bool(self.student) == bool(self.staff):
            raise ValidationError(
                "Assign this checkout to exactly one borrower: a Student OR a Staff member."
            )

        # (2) Prevent multiple open checkouts for the same device
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
        status = "Returned" if self.returned_at else "Out"
        return f"{self.device.asset_tag} → {self.borrower} ({status})"

    def get_absolute_url(self):
        return reverse("checkout-detail", args=[self.pk])
