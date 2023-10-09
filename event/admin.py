from django.contrib import admin

from .models import Event, EventRegistration


class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "arranged_by", "start", "end")
    list_filter = ("arranged_by",)
    search_fields = (
        "name",
        "arranged_by__username",
    )


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "event")
    list_filter = ("event__name",)
    search_fields = ("user__username", "event__name")


admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
