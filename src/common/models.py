from django.db import models
from django.utils import timezone


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        timezone_now = timezone.now()

        if self._state.adding:
            self.created_at = timezone_now

        self.updated_at = timezone_now

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
