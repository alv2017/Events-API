from datetime import date, datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class EventQuerySet(models.QuerySet):
    def published_events(self):
        return self.filter(is_published=True)

    def unpublished_events(self):
        return self.filter(is_published=False)

    def today_events(self):
        ct = timezone.now()
        return self.filter(start__date=ct.date(), is_published=True)

    def past_events(self):
        ct = timezone.now()
        return self.filter(start__lt=ct, is_published=True)

    def future_events(self):
        ct = timezone.now()
        return self.filter(start__gt=ct, is_published=True)


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def published_events(self):
        return self.get_queryset().published_events()

    def unpublished_events(self):
        return self.get_queryset().unpublished_events()

    def today_events(self):
        return self.get_queryset().today_events()

    def past_events(self):
        return self.get_queryset().past_events()

    def future_events(self):
        return self.get_queryset().future_events()


class Event(models.Model):
    name = models.CharField(_("Event Name"), max_length=32, unique=True)
    description = models.CharField(
        _("Event Details"), max_length=1024, blank=True, null=True, default=""
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    registration_deadline = models.DateTimeField(
        _("Registration Deadline"), blank=True, null=True
    )
    number_of_seats = models.IntegerField(_("Number of seats"), default=0)
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
    events = EventManager()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ("-start", "-end")

    def __str__(self):
        return f"{self.start.strftime('%Y-%m-%d')}, {self.start.strftime('%H:%M')}, {self.name}"

    @property
    def total_registrations(self):
        return self.registrations.count()


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Registration for Event"
        verbose_name_plural = "Registration for Event"
        unique_together = ("event", "user")

    def __str__(self):
        return f"{str(self.user)} attends {str(self.event)}"
