from django.core.handlers.wsgi import WSGIRequest

from django_activity_tracker import models as activity_models
from django_activity_tracker import views as activity_views
from tests import models, serializers


class ItemsBaseViewSet(activity_views.ActivityAwareModelViewSet):
    """Test viewset."""

    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


class ItemsViewSetWithGetActionTypeImpl(ItemsBaseViewSet):
    """Test viewset."""

    def get_action_type(self, request: WSGIRequest):
        f"""{super().get_action_type.__doc__}"""
        return activity_models.ActivityLogType.objects.get_or_create(
            name=request.method, label="test"
        )[0]


class ItemsViewSetWithoutTracking(ItemsBaseViewSet):
    """Test viewset."""
