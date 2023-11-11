"""Django Activity Tracker application config."""

from django.apps import AppConfig


class DjangoActivityTrackerConfig(AppConfig):
    """Django Activity Tracker default config."""

    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_activity_tracker"
    verbose_name = "Django Activity Tracker"
