from django.db import models
from django.utils.translation import ugettext_lazy as _


class EventType(models.Model):
    key = models.CharField(
        verbose_name=_("Key (use for front)"),
        null=False,
        blank=False,
        max_length=100,
        unique=True
    )

    name = models.CharField(
        verbose_name=_("Name"),
        null=False,
        blank=False,
        max_length=100
    )


class Event(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        null=False,
        blank=False,
        max_length=100
    )

    place = models.ForeignKey(
        'artwork.Place',
        verbose_name=_("Place"),
        related_name='events',
        on_delete=models.CASCADE
    )

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True
    )

    picture = models.ImageField(
        verbose_name=_("Picture"),
        null=True,
        blank=True
    )

    link = models.URLField(
        verbose_name=_("Url to registration page"),
        null=True,
        blank=True,
        max_length=1024
    )

    event_type = models.ForeignKey(
        'EventType',
        verbose_name=_("Event Type"),
        related_name='events',
        on_delete=models.CASCADE
    )
