from rest_framework import serializers

from django_activity_tracker import serializers as activity_serializers
from tests import models


class ItemSerializer(
    activity_serializers.AdminOnlyFieldsSerializerMixin, serializers.ModelSerializer
):
    """Serializer for testing."""

    class Meta:
        model = models.Item
        fields = "__all__"
