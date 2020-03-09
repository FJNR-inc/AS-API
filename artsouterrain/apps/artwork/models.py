import uuid

from django.db import models
from django.db.models import F
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

    link = models.TextField(
        verbose_name=_("Url to partner"),
        null=True,
        blank=True,
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

    bio = models.TextField(
        verbose_name=_("Bio"),
        blank=True,
        null=True,
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

    plan = models.ImageField(
        verbose_name=_("Picture"),
        null=True,
        blank=True
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

    def __str__(self):
        return self.name


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

    plan = models.ImageField(
        verbose_name=_("Plan"),
        null=True,
        blank=True
    )

    index_itinerary = models.IntegerField(
        verbose_name=_("Index Itinerary"),
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

    creation_year = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    qr_code_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_('QR Code Token')
    )

    off_road = models.BooleanField(
        verbose_name=_('Off road'),
        default=True
    )

    def __str__(self):
        return f'{self.name}'

    @property
    def next_artwork(self):
        if self.index_itinerary:
            return Artwork.objects\
                .filter(index_itinerary__gt=self.index_itinerary)\
                .order_by('index_itinerary').first()
        else:
            return None

    @property
    def previous_artwork(self):
        if self.index_itinerary:
            return Artwork.objects\
                .filter(index_itinerary__lt=self.index_itinerary)\
                .order_by('-index_itinerary').first()
        else:
            return None


class ArtworkMedia(models.Model):

    artwork = models.ForeignKey(
        Artwork,
        related_name='medias',
        verbose_name=_('Artwork'),
        on_delete=models.CASCADE
    )

    file = models.FileField(
        verbose_name=_('File')
    )

    media_type = models.CharField(
        max_length=250,
        verbose_name=_('Madia Type')
    )

    detail = models.TextField(
        verbose_name=_('Detail'),
        null=True,
        blank=True
    )

    @property
    def name(self):
        return self.file.name

    def __str__(self):
        return f'{self.artwork} - {self.file.name}'


class ArtworkVisit(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        related_name='visits',
        verbose_name=_('Artwork'),
        on_delete=models.CASCADE
    )

    email = models.CharField(
        max_length=255,
        verbose_name=_("Participant email")
    )

    visit_date = models.DateTimeField(
        verbose_name=_('Visit Date'),
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.artwork} - {self.email}'


class UpdateData(models.Model):

    create_date = models.DateTimeField(
        verbose_name=_('Create date'),
        auto_now_add=True
    )

    places_text = models.TextField(null=True, blank=True)
    partner_type_text = models.TextField(null=True, blank=True)
    artwork_types_text = models.TextField(null=True, blank=True)
    partner_text = models.TextField(null=True, blank=True)
    artworks_text = models.TextField(null=True, blank=True)
    artists_text = models.TextField(null=True, blank=True)
    events_text = models.TextField(null=True, blank=True)
    event_types_text = models.TextField(null=True, blank=True)
    questions_text = models.TextField(null=True, blank=True)
    choices_text = models.TextField(null=True, blank=True)

    def update_data(self):

        from artsouterrain.apps.artwork.update_data import UpdateDataProcess
        UpdateDataProcess(self).run()

