"""Django Activity Tracker URLs configuration.

The activity logs of your users can be accessed at `/activity-logs/`.
"""

from django.conf import settings
from rest_framework import routers

from . import views

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()
router.register(r"activity-logs", views.ActivityLogViewSet, basename="activity-logs")

urlpatterns = router.urls
