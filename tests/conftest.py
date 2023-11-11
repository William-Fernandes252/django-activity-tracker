import django
import pytest

DEFAULT_DEV_SETTINGS = dict(
    DEBUG_PROPAGATE_EXCEPTIONS=True,
    DATABASES={
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
        "secondary": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
    },
    SITE_ID=1,
    SECRET_KEY="not very secret in tests",
    USE_I18N=True,
    STATIC_URL="/static/",
    ROOT_URLCONF="tests.urls",
    MIDDLEWARE=(
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ),
    INSTALLED_APPS=(
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.staticfiles",
        "rest_framework",
        "tests",
        "django_activity_tracker",
    ),
    PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
    ACTIVITY_LOG_MODEL=None,
    USE_L10N=django.VERSION < (4, 0),
)


def pytest_configure(config):
    """Pytest configure hook."""
    from django.conf import settings

    # USE_L10N is deprecated, and will be removed in Django 5.0.
    settings.configure(
        **DEFAULT_DEV_SETTINGS,
    )

    django.setup()


@pytest.fixture
def item(db):
    """Create a test item."""
    from tests import models

    return models.Item.objects.create(description="Test item")


@pytest.fixture
def user(db):
    """Create a test user."""
    from django.contrib.auth import get_user_model

    return getattr(get_user_model().objects, "create_user")(
        "test", "test@test.com", "test"
    )


@pytest.fixture
def admin(user):
    """Create a test user."""
    user.is_staff = True
    user.is_superuser = True
    user.save()


@pytest.fixture
def activity_log(db, item, user):
    """Create a test activity log."""
    from django_activity_tracker import models

    return models.ActivityLog.objects.create(
        content_object=item,
        type=models.ActivityLogType.objects.get_or_create(name="test", label="Test")[0],
        user=user,
    )
