from django.contrib.auth.models import AbstractBaseUser
from django.test import RequestFactory

from django_activity_tracker import models as activity_models
from django_activity_tracker import serializers as activity_serializers
from tests import serializers as test_serializers


class TestAdminOnlyFieldsSerializerMixin:
    """Test admin only fields serializer mixin."""

    def test_it_leaves_protected_fields_available_for_admin(
        self, admin: AbstractBaseUser, rf: RequestFactory
    ):
        """It removes admin only fields."""
        request = rf.get("/")
        request.user = admin
        serializer = test_serializers.ItemSerializer(
            admin_only=["description"], context={"request": request}
        )
        assert "description" in serializer.fields

    def test_it_removes_non_admin_only_fields(
        self, user: AbstractBaseUser, rf: RequestFactory
    ):
        """It removes non admin only fields."""
        request = rf.get("/")
        request.user = user
        serializer = test_serializers.ItemSerializer(
            admin_only=["description"], context={"request": request}
        )
        assert "description" not in serializer.fields


class TestActivitySerializer:
    """Test activity serializer."""

    def test_it_serializes_type_to_its_name(
        self, activity_log: activity_models.ActivityLog
    ):
        """Activity `type` should be the name of the action type."""
        serializer = activity_serializers.ActivityLogSerializer(instance=activity_log)
        assert serializer.data["type"] == getattr(activity_log.type, "name")

    def test_it_serializes_content_type_to_its_name(
        self, activity_log: activity_models.ActivityLog
    ):
        """Activity `content_type` should be the name of the action type."""
        serializer = activity_serializers.ActivityLogSerializer(instance=activity_log)
        assert serializer.data["content_type"] == getattr(
            activity_log.content_type, "name"
        )

    def test_it_serializes_user_to_its_email(
        self, activity_log: activity_models.ActivityLog
    ):
        """Activity `content_type` should be the name of the action type."""
        serializer = activity_serializers.ActivityLogSerializer(instance=activity_log)
        assert serializer.data["user"] == getattr(activity_log.user, "email")

    def test_it_removes_non_admin_only_fields(
        self,
        activity_log: activity_models.ActivityLog,
        user: AbstractBaseUser,
        rf: RequestFactory,
    ):
        """It removes non admin only fields."""
        request = rf.get("/")
        request.user = user
        serializer = activity_serializers.ActivityLogSerializer(
            instance=activity_log, admin_only=["user"], context={"request": request}
        )
        assert "user" not in serializer.data
