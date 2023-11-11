import pytest
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory
from rest_framework.response import Response

from tests import models, views


class TestActivityAwareAPIView:
    """Test the registering of user actions by the `ActivityAwareAPIView`."""

    @pytest.fixture
    def view_request(self, rf: RequestFactory):
        """Creates a test request with an anonymous user."""
        request = rf.get("/1/")
        request.user = AnonymousUser()
        return request

    @pytest.fixture
    def authenticated_request(self, view_request: WSGIRequest, user: AbstractBaseUser):
        """Creates a test authenticated request."""
        view_request.user = user
        return view_request

    class TestGetLogMessage:
        def test_it_builds_message_with_username_and_timestamp(
            self, authenticated_request: WSGIRequest
        ):
            """It should build a message with the username and timestamp."""
            viewset = views.ItemsViewSetWithGetActionTypeImpl()
            log_message = viewset.get_log_message(authenticated_request)
            for content in [
                str(authenticated_request.user),
                authenticated_request.method,
            ]:
                assert content in log_message

        def test_it_returns_default_message_if_set(
            self, authenticated_request: WSGIRequest
        ):
            """It should return the default message if set."""
            log_message = "success"

            viewset = views.ItemsViewSetWithGetActionTypeImpl()
            viewset.log_message = log_message
            assert viewset.get_log_message(authenticated_request) == log_message

    class TestLogEntryPersistence:
        @pytest.fixture
        def viewset(self):
            """Viewset fixture."""
            return views.ItemsViewSetWithGetActionTypeImpl.as_view({"get": "retrieve"})

        def test_it_persists_log_entry_in_authenticated_request(
            self,
            rf: RequestFactory,
            item: models.Item,
            user: AbstractBaseUser,
            viewset,
        ):
            """It should persists the log entry."""
            request = rf.get(f"items-with-tracking/{item.pk}")
            request.user = user
            response: Response = viewset(request, pk=item.pk)
            assert response.status_code == 200
            assert item.actions.count() == 1

        def test_it_logs_entry_contains_user(
            self,
            rf: RequestFactory,
            item: models.Item,
            user: AbstractBaseUser,
            viewset,
        ):
            """The log entry should contain the user associated with the request."""
            request = rf.get(f"items-with-tracking/{item.pk}")
            request.user = user
            viewset(request, pk=item.pk)
            assert item.actions.first().user == user

        def test_it_logs_entry_with_the_correct_type(
            self,
            rf: RequestFactory,
            item: models.Item,
            user: AbstractBaseUser,
            viewset,
        ):
            """The log entry must contain the action type."""
            request = rf.get(f"items-with-tracking/{item.pk}")
            request.user = user
            viewset(request, pk=item.pk)
            assert item.actions.first().type.name == "GET"

        def test_it_dont_persists_log_entry_in_anonymous_request(
            self,
            rf: RequestFactory,
            item: models.Item,
        ):
            """It should not persists log entries in an anonymous request."""
            viewset = views.ItemsViewSetWithGetActionTypeImpl.as_view(
                {"get": "retrieve"}
            )
            request = rf.get(f"items-with-tracking/{item.pk}")
            request.user = AnonymousUser()
            response: Response = viewset(request, pk=item.pk)
            assert response.status_code == 200
            assert item.actions.count() == 0
