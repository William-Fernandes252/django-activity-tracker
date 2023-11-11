"""Models for testing."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_activity_tracker.models import ActivityAwareModel


class DjangoActivityTrackerTestModel(ActivityAwareModel):
    """Base for test models that sets app_label, so they play nicely."""

    class Meta:
        app_label = "tests"
        abstract = True


class Item(DjangoActivityTrackerTestModel):
    """Test model."""

    description = models.CharField(
        max_length=100,
        verbose_name=_("Text comes here"),
        help_text=_("Text description."),
    )
