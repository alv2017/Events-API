from datetime import date, datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class PublishedEventsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class TodayEventsManager(models.Manager):
    def get_queryset(self):
        ct = timezone.now()
        return super().get_queryset().filter(start__date=ct.date(), is_published=True)


class PastEventsManager(models.Manager):
    def get_queryset(self):
        ct = timezone.now()
        return super().get_queryset().filter(start__lt=ct, is_published=True)


class FutureEventsManager(models.Manager):
    def get_queryset(self):
        ct = timezone.now()
        return super().get_queryset().filter(start__gt=ct, is_published=True)


class Event(models.Model):
    name = models.CharField(_("Event Name"), max_length=32, unique=True)
    description = models.CharField(
        _("Event Details"), max_length=1024, blank=True, null=True, default=""
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    arranged_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="events",
        related_query_name="event",
    )
    is_published = models.BooleanField(default=True)
    registrations = models.ManyToManyField(
        User,
        through="EventRegistration",
        through_fields=("event", "user"),
        related_name="registrations",
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    today_events = TodayEventsManager()
    past_events = PastEventsManager()
    future_events = FutureEventsManager()
    published_events = PublishedEventsManager()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ("-start", "-end")

    def __str__(self):
        return f"{self.start.strftime('%Y-%m-%d')}, {self.start.strftime('%H:%M')}, {self.name}"


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Registration for Event"
        verbose_name_plural = "Registration for Event"
        unique_together = ("event", "user")

    def __str__(self):
        return f"{str(self.user)} attends {str(self.event)}"
