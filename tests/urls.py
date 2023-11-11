from django.urls import include, path
from rest_framework import routers

from tests import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(
    r"items-with-tracking",
    views.ItemsViewSetWithGetActionTypeImpl,
    basename="items-with-tracking",
)
router.register(
    r"items-without-tracking",
    views.ItemsViewSetWithoutTracking,
    basename="items-without-tracking",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("django_activity_tracker.urls")),
]
