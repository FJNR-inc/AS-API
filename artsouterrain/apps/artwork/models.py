from django.db import models
from django.utils.translation import ugettext_lazy as _


class PartnerType(models.Model):
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


class Partner(models.Model):
    name = models.CharField(
        verbose_name=_("Partner Name"),
        null=False,
        blank=False,
        max_length=100
    )

    logo = models.ImageField(
        verbose_name=_("Logo"),
        null=True,
        blank=True
    )

    link = models.URLField(
        verbose_name=_("Url to partner"),
        null=True,
        blank=True,
        max_length=1024
    )

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True
    )

    partner_type = models.ForeignKey(
        PartnerType,
        verbose_name=_("Type"),
        on_delete=models.CASCADE
    )


class Artist(models.Model):
    first_name = models.CharField(
        verbose_name=_("First name"),
        null=False,
        blank=False,
        max_length=100
    )

    last_name = models.CharField(
        verbose_name=_("Last name"),
        null=True,
        blank=True,
        max_length=100
    )

    country = models.CharField(
        verbose_name=_("Country"),
        null=True,
        blank=True,
        max_length=100
    )

    picture = models.ImageField(
        verbose_name=_("Picture"),
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Place(models.Model):

    name = models.CharField(
        verbose_name=_("Place Name"),
        null=False,
        blank=False,
        max_length=100
    )

    def __str__(self):
        return f'{self.name}'


class ArtworkType(models.Model):
    name = models.CharField(
        verbose_name=_("Artwork Type"),
        null=False,
        blank=False,
        max_length=100
    )


class Artwork(models.Model):

    name = models.CharField(
        verbose_name=_("Name"),
        null=False,
        blank=False,
        max_length=100
    )

    artist = models.ForeignKey(
        Artist,
        verbose_name=_("artist"),
        related_name='artworks',
        on_delete=models.CASCADE
    )

    place = models.ForeignKey(
        Place,
        verbose_name=_("Place"),
        related_name='artworks',
        on_delete=models.CASCADE
    )

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        verbose_name=_("Picture"),
        null=True,
        blank=True
    )

    artwork_type = models.ForeignKey(
        ArtworkType,
        verbose_name=_("Artwork Type"),
        related_name='artworks',
        on_delete=models.CASCADE
    )

    level = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    latitude = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    longitude = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name}'
