from typing import Callable

import pytest
from django.contrib.auth.models import AbstractBaseUser

from django_activity_tracker import models as activity_models
from tests import models

pytestmark = pytest.mark.django_db


class TestItem:
    """Tracking of users actions on a generic model."""

    @pytest.fixture
    def activity_log_type_factory(
        self, db
    ) -> Callable[[str, str], activity_models.ActivityLogType]:
        """Returns a callable to create action types."""

        def factory(name, label):
            return activity_models.ActivityLogType.objects.create(
                name=name, label=label
            )

        return factory

    def test_it_creates_activity_generic_relationship(
        self,
        item: models.Item,
        user: AbstractBaseUser,
        activity_log_type_factory: Callable[
            [str, str], activity_models.ActivityLogType
        ],
    ):
        """It should create an activity generic relationship."""
        action = activity_models.ActivityLog.objects.create(
            content_object=item,
            type=activity_log_type_factory("create", "Create"),
            user=user,
        )
        item.refresh_from_db()
        assert getattr(item, "actions") and action in item.actions.all()

    def test_related_query_returns_tracked_objects(
        self,
        item: models.Item,
        user: AbstractBaseUser,
        activity_log_type_factory: Callable[
            [str, str], activity_models.ActivityLogType
        ],
    ):
        """It should return all tracked objects."""
        activity_models.ActivityLog.objects.create(
            content_object=item,
            type=activity_log_type_factory("create", "Create"),
            user=user,
        )
        item.refresh_from_db()
        assert activity_models.ActivityLog.objects.filter(tests_item=item).exists()
