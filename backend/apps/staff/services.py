
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.centres.models import Centre
from .models import StaffIdSequence


@transaction.atomic
def generate_staff_id(centre_id):
    """
    Generate a unique Staff ID for a centre.

    Example: NGLST001, NGLST002, NGLST003

    Locking the Centre row serializes ID allocation for
    concurrent registrations at the same centre.
    """

    centre = (
        Centre.objects
        .select_for_update()
        .get(pk=centre_id)
    )

    if not centre.is_active:
        raise ValidationError("Cannot generate an ID for an inactive centre.")

    sequence, _ = StaffIdSequence.objects.get_or_create(
        centre=centre
    )

    sequence = (
        StaffIdSequence.objects
        .select_for_update()
        .get(pk=sequence.pk)
    )

    sequence.last_number += 1

    sequence.save(
        update_fields=["last_number", "updated_at"]
    )

    return f"{centre.code}ST{sequence.last_number:03d}"
