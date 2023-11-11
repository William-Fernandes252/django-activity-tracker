"""Models for Django Activity Tracker."""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ActivityLogType(models.Model):
    """Model for storing activity types."""

    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)


class StatusChoices(models.TextChoices):
    """Possible statuses of an user action."""

    SUCCESS = "SC"
    FAILED = "FD"


class ActivityLog(models.Model):
    """Default activity log model.

    Note that by default the actions of a user are deleted
    when the user is deleted (the relation uses `on_delete=models.CASCADE`).
    """

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="actions"
    )
    type = models.ForeignKey(ActivityLogType, on_delete=models.PROTECT)
    status = models.CharField(max_length=2, choices=StatusChoices.choices)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Actions"
        ordering = ["-timestamp"]


class ActivityAwareModel(models.Model):
    """Abstract model that can be used to track users interactions with a model.

    It sets a generic relation to the `ActivityLog` model (through the field `actions`)
    where the `related_query_name` is set to `%(app_label)s_%(class)s`.
    """

    actions = GenericRelation(ActivityLog, related_query_name="%(app_label)s_%(class)s")

    class Meta:
        abstract = True
