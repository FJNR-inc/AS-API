from django.contrib import admin

from artsouterrain.apps.event.models import EventType, Event

admin.site.register(Event)
admin.site.register(EventType)
