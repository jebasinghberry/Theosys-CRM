from django.contrib import admin

from .models import (
    StaffProfile,
    StaffEmergencyContact,
    StaffTeamAssignment,
    StaffIdSequence,
)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):

    list_display = (
        "staff_id",
        "full_name",
        "centre",
        "team",
        "mobile_number",
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "centre__code",
        "team__name",
    )

    list_filter = (
        "centre",
        "team",
        "is_active",
    )

    readonly_fields = (
        "staff_id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Account", {
            "fields": ("user", "staff_id")
        }),
        ("Centre Assignment", {
            "fields": ("centre", "team", "designation")
        }),
        ("Personal Information", {
            "fields": (
                "middle_name",
                "date_of_birth",
                "sex",
                "mobile_number",
                "photo",
            )
        }),
        ("Address", {
            "fields": (
                "address_line_1",
                "address_line_2",
                "landmark",
                "city",
                "postal_code",
            )
        }),
        ("Employment", {
            "fields": (
                "date_of_joining",
                "is_active",
                "created_by",
            )
        }),
        ("System Information", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(StaffEmergencyContact)
class StaffEmergencyContactAdmin(admin.ModelAdmin):

    list_display = (
        "staff",
        "name",
        "relationship",
        "mobile_number",
    )

    search_fields = (
        "staff__user__username",
        "name",
        "mobile_number",
    )


@admin.register(StaffTeamAssignment)
class StaffTeamAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "staff",
        "centre",
        "team",
        "assigned_from",
        "assigned_until",
    )

    list_filter = ("centre", "team")

    search_fields = (
        "staff__user__username",
        "team__name",
    )

    readonly_fields = ("created_at", "updated_at")


@admin.register(StaffIdSequence)
class StaffIdSequenceAdmin(admin.ModelAdmin):

    list_display = (
        "centre",
        "last_number",
        "updated_at",
    )

    readonly_fields = (
        "centre",
        "last_number",
        "created_at",
        "updated_at",
    )

