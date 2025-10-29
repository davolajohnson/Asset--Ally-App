from django.db import models

class Device(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE","Available"),
        ("CHECKED_OUT","Checked Out"),
        ("REPAIR","Repair"),
        ("LOST","Lost"),
        ("RETIRED","Retired"),
    ]
    CONDITION_CHOICES = [
        ("NEW","New"),
        ("GOOD","Good"),
        ("FAIR","Fair"),
        ("POOR","Poor")
    ]

    asset_tag = models.CharField(max_length=40, unique=True)
    serial_number = models.CharField(max_length=60, unique=True)
    manufacturer = models.CharField(max_length=60, blank=True)
    model = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="GOOD")

    def __str__(self):
        return f"{self.asset_tag} — {self.model or 'Device'}"

