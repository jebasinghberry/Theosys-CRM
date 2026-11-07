from django.contrib import admin

from .models import (
    Centre,
    Team,
    Batch,
    BatchSlot,
    CentreUserAccess,
)


@admin.register(Centre)
class CentreAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "city",
        "phone",
        "is_active",
    )

    search_fields = ("code", "name", "city")

    list_filter = ("is_active", "city")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "centre",
        "is_active",
    )

    search_fields = ("name", "centre__code")

    list_filter = ("centre", "is_active")


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "centre",
        "is_active",
    )

    search_fields = ("name", "centre__code")

    list_filter = ("centre", "is_active")


@admin.register(BatchSlot)
class BatchSlotAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "batch",
        "start_time",
        "end_time",
        "capacity",
        "is_active",
    )

    list_filter = ("batch", "is_active")


@admin.register(CentreUserAccess)
class CentreUserAccessAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "centre",
        "is_active",
        "assigned_by",
    )

    search_fields = (
        "user__username",
        "centre__code",
    )

    list_filter = ("centre", "is_active")