from rest_framework import serializers

from artsouterrain.apps.artwork.models import Partner, PartnerType, Artwork, \
    ArtworkType, Place, Artist, ArtworkMedia, ArtworkVisit


class PartnerTypeSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = PartnerType
        fields = '__all__'


class PartnerSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    partner_type = PartnerTypeSerializer(many=False)

    class Meta:
        model = Partner
        fields = '__all__'


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Artist
        fields = '__all__'


class ArtistSerializerSmall(ArtistSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Artist
        fields = ('id', 'url', 'first_name','last_name', 'country')


class PlaceSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Place
        fields = '__all__'


class ArtworkTypeSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = ArtworkType
        fields = '__all__'


class ArtworkSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Artwork
        fields = '__all__'


class ArtworkSerializerSmall(ArtworkSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Artwork
        fields = ('id', 'url', 'name', 'picture')


class ArtworkSerializerDetail(ArtworkSerializer):

    id = serializers.ReadOnlyField()

    artist = ArtistSerializer(many=False)

    place = PlaceSerializer(many=False)

    artwork_type = ArtworkTypeSerializer(many=False)

    next_artwork = ArtworkSerializerSmall(
        many=False,
        read_only=True,
        allow_null=True
    )

    previous_artwork = ArtworkSerializerSmall(
        many=False,
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Artwork
        fields = '__all__'


class ArtworkSerializerList(ArtworkSerializerDetail):

    id = serializers.ReadOnlyField()

    artist = ArtistSerializerSmall()

    class Meta:
        model = Artwork
        fields = (
            'id', 'url', 'name', 'picture',
            'place', 'artist', 'longitude', 'latitude')


class ArtworkMediaSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = ArtworkMedia
        fields = '__all__'


class ArtworkVisitSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = ArtworkVisit
        fields = '__all__'
