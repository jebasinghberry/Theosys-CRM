from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q, F

from apps.common.models import TimeStampedModel


class Centre(TimeStampedModel):

    code = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9]+$",
                message="Centre code must contain only letters and numbers."
            )
        ]
    )

    name = models.CharField(max_length=150)

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(
        max_length=255,
        blank=True
    )

    landmark = models.CharField(
        max_length=150,
        blank=True
    )

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)

    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "centres"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Team(TimeStampedModel):

    centre = models.ForeignKey(
        Centre,
        on_delete=models.PROTECT,
        related_name="teams"
    )

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "teams"
        ordering = ["centre", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["centre", "name"],
                name="uniq_team_name_per_centre"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.centre.code}"


class Batch(TimeStampedModel):

    centre = models.ForeignKey(
        Centre,
        on_delete=models.PROTECT,
        related_name="batches"
    )

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "batches"
        ordering = ["centre", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["centre", "name"],
                name="uniq_batch_name_per_centre"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.centre.code}"


class BatchSlot(TimeStampedModel):

    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        related_name="slots"
    )

    name = models.CharField(max_length=100)

    start_time = models.TimeField()
    end_time = models.TimeField()

    capacity = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "batch_slots"
        ordering = ["start_time"]

        constraints = [
            models.UniqueConstraint(
                fields=["batch", "name"],
                name="uniq_slot_name_per_batch"
            ),
            models.CheckConstraint(
                condition=Q(end_time__gt=F("start_time")),
                name="valid_batch_slot_time"
            ),
            models.CheckConstraint(
                condition=Q(capacity__gt=0),
                name="valid_batch_slot_capacity"
            )
        ]

    def __str__(self):
        return f"{self.batch.name} - {self.name}"


class CentreUserAccess(TimeStampedModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="centre_access"
    )

    centre = models.ForeignKey(
        Centre,
        on_delete=models.PROTECT,
        related_name="user_access"
    )

    is_active = models.BooleanField(default=True)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="granted_centre_access"
    )

    class Meta:
        db_table = "centre_user_access"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "centre"],
                name="uniq_user_centre_access"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.centre.code}"
