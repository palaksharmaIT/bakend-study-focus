from django.db import models
from django.contrib.auth.models import User


class BlockedWebsite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="blocked_websites"
    )

    domain = models.CharField(
        max_length=255
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "domain")

    def __str__(self):
        return f"{self.user.username} - {self.domain}"


class FocusSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    duration = models.IntegerField(
        default=0
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.duration} minutes"