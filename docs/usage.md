# Usage

To use Django Activity Tracker in a project

-   include it in your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...,
    "django_activity_tracker",
    ...
]
```

-   make the migrations to create the app models

```bash
python manage.py makemigrations
```

-   execute the migrations

```bash
python manage.py migrate
```

Now, in order to track the users interations with one of your models

-   Inherit from `django_activity_tracker.models.ActivityAwareModel`

```python
class YourModel(ActivityAwareModel):
    ...
```

-   Use the `django_activity_tracker.views.ActivityAwareAPIView` in the viewset of your model

```python
from rest_framework.viewsets import ModelViewSet

class YourModelViewSet(ActivityAwareAPIView, ModelViewSet):
    ...
```

-   Implement the method `get_action_type(self, request)` in the viewset

```python
from rest_framework.viewsets import ModelViewSet

class YourModelViewSet(ActivityAwareAPIView, ModelViewSet):
    def get_action_type(self, request):
        return ActivityType.objects.get_or_create(
            name=f"{request.method} {request.path}",
            label=f"{request.method.tolower()}"
        )[0]
```

This method is responsible to determine the meaning of the users actions through the viewset. It must have a name, and a label.

Now the users actions in any instance of your model can be queried through their `actions` attribute (its a `GenericRelation` field).
