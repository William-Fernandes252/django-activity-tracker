from django.contrib import admin

from .models import ActivityLog


class ActivityLogAdmin(admin.ModelAdmin):
    """Admin for `ActivityLog`."""

    list_display = (
        "id",
        "user",
        "type",
        "status",
        "description",
        "timestamp",
        "content_type",
        "object_id",
    )
    list_filter = ("user__email", "object_id", "content_type", "timestamp")
    search_fields = ("user__email", "object_id", "content_type__model")


admin.site.register(ActivityLog, ActivityLogAdmin)
