"""Serializers for Django Activity Tracker."""

from django.conf import settings
from rest_framework import serializers

from django_activity_tracker.models import ActivityLog


class AdminOnlyFieldsSerializerMixin:
    """Serializer mixin to remove fields if the user is not an admin.

    You may want to restrict who can access the actions of the users of your
    application. This is a utility serializer mixin to remove fields if the
    user is not an admin. In order to use it, you have to pass the list of
    fields that you want to protect in the `admin_only` kwarg. Note that you
    have to pass the request in the `context` kwarg so that the serializer
    can know if the request is authenticated and if the user is an admin.

    ```

    # Usage:

    class MyActivityModelSerializer(AdminOnlyFieldsSerializerMixin, ActivitySerializer):
        ...

    serializer = MyActivityModelSerializer(
        context={"request": request},
        admin_only=["user", "content_type"],
    )

    ```
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the serializer."""
        admin_only_fields = set(
            kwargs.pop(
                "admin_only", getattr(self.Meta, "admin_only", [])  # type: ignore
            )
        )
        super().__init__(*args, **kwargs)

        context = kwargs.get("context")
        if not context:
            return

        request = context.get("request")
        if not request:
            return

        if request.user and not getattr(request.user, "is_superuser", False):
            for field_name in admin_only_fields:
                self.fields.pop(field_name)  # type: ignore


class ActivityLogSerializer(
    AdminOnlyFieldsSerializerMixin, serializers.ModelSerializer
):
    """Serializer for Activity model.

    It shows all fields by default. The user is represented by its email and
    the `content_type` is the name of the tracked model.
    """

    id = serializers.CharField(read_only=True)
    type = serializers.CharField(source="type.name", read_only=True)
    content_type = serializers.CharField(source="content_type.name", read_only=True)
    user = serializers.EmailField(source="user.email")

    class Meta:
        model = settings.ACTIVITY_LOG_MODEL or ActivityLog
        fields = "__all__"
