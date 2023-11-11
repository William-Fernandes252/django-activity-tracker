## Models

This is the current representation for a user action

```python
class ActivityLog(models.Model):
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
```

## Views

In order to read the activity logs of your application, add the app urls to your root url configuration

```python
urlpatterns = [
    ...,
    path("", include("django_activity_tracker.urls")),
    ...
]
```

Or access the admin site, which now contains a table showing the logs. There you can filter the actions by user, status, target object and type, and sort by timestamp.
