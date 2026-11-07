from django.db import models


class TimeStampedModel(models.Model):
    """
    Common fields for project database models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
