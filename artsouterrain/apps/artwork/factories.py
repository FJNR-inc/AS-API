import factory

from artsouterrain.apps.artwork.models import (
    ArtworkType,
    Artwork,
    Artist,
    Place,
)


class ArtworkFactory(factory.DjangoModelFactory):
    class Meta:
        model = Artwork

    name = factory.Sequence('artwork{0}'.format)

    @classmethod
    def __init__(self, **kwargs):
        kwargs.pop('artwork_type', None)
        kwargs.pop('artist', None)

        artwork = super(ArtworkFactory, self).__init__(self, **kwargs)
        artwork.save()

class ArtworkTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = ArtworkType

    name = factory.Sequence('artworkType{0}'.format)


class ArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = Artist

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class PlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Place

    name = factory.Sequence('place{0}'.format)

