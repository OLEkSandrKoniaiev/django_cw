from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    INACTIVE = 'Inactive', 'Inactive'
    PENDING_REVIEW = 'Pending Review', 'Pending Review'
    REJECTED = 'Rejected', 'Rejected'
