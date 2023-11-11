"""Views for Django Activity Tracker."""

from __future__ import annotations

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from rest_framework import generics, mixins, viewsets
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from django_activity_tracker import models, serializers


class ActivityAwareAPIView(generics.GenericAPIView):
    """Generic APIView to register logs of user actions in the database."""

    log_message: str | None = None

    def get_action_type(self, request: HttpRequest) -> models.ActivityLogType | None:
        """Gets the activity type to be logged for the users request.

        Its receives the request instance (`HttpRequest` object) and should return
        either the action type object to be registered, or `None`, if the user action
        should not be registered.

        You could use


        ```
        return ActivityType.objects.get_or_create(
            name=f"{request.method} {request.path}",
            label=f"{request.method.tolower()}"
        )[0]
        ```

        for example, in order to create the action type if it doesn't exist,
        or use the viewset action name.

        Args:
            request (HttpRequest): _description_

        Returns:
            models.ActivityType | None: The action type to be logged, or None,
            if the user action should not be registered.
        """
        return None

    def _build_log_message(self, request: HttpRequest):
        return (
            f"User {self._get_user(request) or '*anonymous*'} requested"
            + " "
            + f"{(request.method or 'GET').upper()} {request.path}."
        )

    def get_log_message(self, request: HttpRequest):
        """Gets the message to be logged.

        Overwrite this method to customize the message to be logged.
        """
        return self.log_message or self._build_log_message(request)

    @staticmethod
    def _get_user(request: HttpRequest):
        return request.user if request.user.is_authenticated else None

    def _persist_log_entry(
        self, request: HttpRequest, response: Response
    ) -> models.ActivityLog | None:
        user = self._get_user(request)
        if not user:
            return None

        action_type = self.get_action_type(request)
        if not action_type:
            return None

        data = {
            "user": self._get_user(request),
            "type": action_type,
            "status": models.StatusChoices.SUCCESS
            if response.status_code < 400
            else models.StatusChoices.FAILED,
            "description": self.get_log_message(request),
        }
        try:
            data["content_type"] = ContentType.objects.get_for_model(
                self.get_queryset().model
            )
            data["content_object"] = self.get_object()
        except (AttributeError, ValidationError):
            data["content_type"] = None
        except AssertionError:
            pass

        return models.ActivityLog.objects.create(**data)

    def finalize_response(self, request, *args, **kwargs):
        """Returns the final response object."""
        response = super().finalize_response(request, *args, **kwargs)
        self._persist_log_entry(request, response)  # type: ignore
        return response


class ActivityAwareModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.ViewSetMixin,
    ActivityAwareAPIView,
):
    """Generic ViewSet to register logs of users interations with a resource.

    It extends the `ViewSetMixin` and `ActivityAwareAPIView`, and includes
    basic CRUD operations.
    """

    pass


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """A basic viewset to list all user actions stored in the database.

    You may want to restrict who can access the actions of the users
    of your application.
    """

    queryset = models.ActivityLog.objects.all()
    serializer_class = serializers.ActivityLogSerializer
