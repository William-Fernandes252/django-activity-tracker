from typing import Any, Dict, Sequence

from pytest_drf import (
    AsUser,
    Returns200,
    UsesDetailEndpoint,
    UsesGetMethod,
    UsesListEndpoint,
    ViewSetTest,
)
from pytest_drf.util import pluralized, url_for
from pytest_lambda import lambda_fixture

from django_activity_tracker import models


def express_activity_log(log: models.ActivityLog) -> Dict[str, Any]:
    """Returns the JSON representation of an activity log."""
    return {
        "id": str(log.pk),
        "type": log.type.name,
        "content_type": log.content_type.name,
        "user": getattr(log.user, "email"),
        "status": log.status,
        "description": log.description,
        "timestamp": log.timestamp.isoformat(),
        "object_id": log.object_id,
    }


express_activity_logs = pluralized(express_activity_log)  # type: ignore


class TestActivityLogViewSet(ViewSetTest):
    """Test ActivityLogViewSet."""

    list_url = lambda_fixture(lambda: url_for("activity-logs-list"))

    detail_url = lambda_fixture(
        lambda activity_log: url_for("activity-logs-detail", pk=activity_log.pk)
    )

    class TestList(  # type: ignore
        UsesListEndpoint, Returns200, UsesGetMethod, AsUser("user")  # type: ignore
    ):
        """Test ActivityLogViewSet list."""

        logs = lambda_fixture(lambda activity_log: [activity_log], autouse=True)

        def test_it_returns_logs(
            self, logs: Sequence[models.ActivityLog], json: Sequence[Dict[str, Any]]
        ):
            """It should return the logs."""
            expected = express_activity_logs(sorted(logs, key=lambda log: log.pk))
            actual = json
            assert expected == actual

    class TestRetrieve(  # type: ignore
        UsesDetailEndpoint, Returns200, UsesGetMethod, AsUser("user")  # type: ignore
    ):
        """Test ActivityLogViewSet retrieve."""

        def test_it_returns_log_by_id(
            self, activity_log: models.ActivityLog, json: Dict[str, Any]
        ):
            """It should return the action."""
            expected = express_activity_log(activity_log)
            actual = json
            assert expected == actual
