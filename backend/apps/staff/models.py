from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    RegexValidator,
)
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.common.models import TimeStampedModel
from apps.centres.models import Centre, Team


def validate_name(value):
    """Allow alphabetic characters from different languages and spaces."""
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError("Only alphabetic characters and spaces are allowed.")


def validate_address(value):
    """Follow the client's address rule: letters, numbers, # and comma."""
    if not all(char.isalnum() or char.isspace() or char in "#," for char in value):
        raise ValidationError(
            "Only letters, numbers, spaces, # and commas are allowed."
        )


def validate_staff_age(value):
    """Staff must be older than 18 as specified in the requirements."""
    today = timezone.localdate()
    age = today.year - value.year - (
        (today.month, today.day) < (value.month, value.day)
    )
    if age <= 18:
        raise ValidationError("Staff member must be above 18 years old.")


mobile_validator = RegexValidator(
    regex=r"^[0-9]{10}$",
    message="Mobile number must contain exactly 10 digits."
)

postal_code_validator = RegexValidator(
    regex=r"^[0-9]{6}$",
    message="PIN code must contain exactly 6 digits."
)


class StaffIdSequence(TimeStampedModel):
    """
    Maintains the next Staff ID number independently for each centre.
    """

    centre = models.OneToOneField(
        Centre,
        on_delete=models.PROTECT,
        related_name="staff_id_sequence",
    )

    last_number = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "staff_id_sequences"

    def __str__(self):
        return f"{self.centre.code}: {self.last_number}"


class StaffProfile(TimeStampedModel):
    """
    Staff employment and personal profile.

    The Django User username is the Staff ID.
    Example: NGLST001
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff_profile",
    )

    centre = models.ForeignKey(
        Centre,
        on_delete=models.PROTECT,
        related_name="staff_members",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="staff_members",
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        validators=[validate_name],
    )

    date_of_birth = models.DateField(
        validators=[validate_staff_age],
    )

    # The exact sex/radio-button options need client confirmation.
    sex = models.CharField(max_length=30)

    mobile_number = models.CharField(
        max_length=10,
        validators=[mobile_validator],
    )

    address_line_1 = models.CharField(
        max_length=255,
        validators=[validate_address],
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        validators=[validate_address],
    )

    landmark = models.CharField(max_length=150, blank=True)

    city = models.CharField(
        max_length=100,
        validators=[validate_name],
    )

    postal_code = models.CharField(
        max_length=6,
        validators=[postal_code_validator],
    )

    photo = models.ImageField(
        upload_to="staff/photos/",
        validators=[FileExtensionValidator(["jpg", "jpeg"])],
    )

    designation = models.CharField(max_length=100, blank=True)

    date_of_joining = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_staff_profiles",
    )

    class Meta:
        db_table = "staff_profiles"
        ordering = ["user__username"]
        indexes = [
            models.Index(fields=["centre", "is_active"]),
            models.Index(fields=["team", "is_active"]),
        ]

    @property
    def staff_id(self):
        return self.user.username

    @property
    def full_name(self):
        return " ".join(
            part for part in [
                self.user.first_name,
                self.middle_name,
                self.user.last_name,
            ] if part
        )

    def clean(self):
        super().clean()

        if self.centre_id and self.team_id:
            if self.team.centre_id != self.centre_id:
                raise ValidationError({
                    "team": "The selected team must belong to the selected centre."
                })

    def __str__(self):
        return f"{self.staff_id} - {self.full_name}"


class StaffEmergencyContact(TimeStampedModel):

    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="emergency_contact",
    )

    name = models.CharField(
        max_length=150,
        validators=[validate_name],
    )

    relationship = models.CharField(
        max_length=80,
        validators=[validate_name],
    )

    mobile_number = models.CharField(
        max_length=10,
        validators=[mobile_validator],
    )

    class Meta:
        db_table = "staff_emergency_contacts"

    def __str__(self):
        return f"Emergency contact - {self.staff.staff_id}"


class StaffIdentity(TimeStampedModel):
    """
    Sensitive identity data.

    Store encrypted ciphertext only. Never put raw Aadhaar/PAN
    values into these fields.
    """

    staff = models.OneToOneField(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="identity",
    )

    aadhaar_ciphertext = models.TextField()
    aadhaar_lookup_hash = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
    )
    aadhaar_last4 = models.CharField(max_length=4)

    # PAN is subject to client confirmation.
    pan_ciphertext = models.TextField(blank=True)
    pan_lookup_hash = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
    )
    pan_last4 = models.CharField(max_length=4, blank=True)

    class Meta:
        db_table = "staff_identities"

    def __str__(self):
        return f"Protected identity - {self.staff.staff_id}"


class StaffTeamAssignment(TimeStampedModel):
    """
    Keeps the history of staff centre/team assignments.
    """

    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.PROTECT,
        related_name="team_assignments",
    )

    centre = models.ForeignKey(
        Centre,
        on_delete=models.PROTECT,
        related_name="staff_assignments",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="staff_assignments",
    )

    assigned_from = models.DateField(default=timezone.localdate)

    assigned_until = models.DateField(
        null=True,
        blank=True,
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_assignments_made",
    )

    class Meta:
        db_table = "staff_team_assignments"
        ordering = ["-assigned_from"]

        constraints = [
            models.UniqueConstraint(
                fields=["staff"],
                condition=Q(assigned_until__isnull=True),
                name="uniq_active_team_assignment_per_staff",
            )
        ]

    def clean(self):
        super().clean()

        if self.team_id and self.centre_id:
            if self.team.centre_id != self.centre_id:
                raise ValidationError({
                    "team": "The team must belong to the selected centre."
                })

        if self.staff_id and self.centre_id:
            if self.staff.centre_id != self.centre_id:
                raise ValidationError({
                    "centre": "The assignment centre must match the staff member's centre."
                })

        if self.assigned_until and self.assigned_from:
            if self.assigned_until < self.assigned_from:
                raise ValidationError({
                    "assigned_until": "End date cannot be before start date."
                })

    def __str__(self):
        return f"{self.staff.staff_id} - {self.team.name}"

