from rest_framework import serializers

from artsouterrain.apps.artwork.serializers import PlaceSerializer, \
    PlaceExtractSerializer
from artsouterrain.apps.event.models import EventType, Event


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = EventType
        fields = '__all__'


class EventSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    event_type = EventTypeSerializer(many=False)
    place = PlaceSerializer(many=False)

    class Meta:
        model = Event
        fields = '__all__'


class EventTypeExtractSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = '__all__'


class EventExtractSerializer(serializers.ModelSerializer):

    event_type = EventTypeExtractSerializer(many=False)

    place = PlaceExtractSerializer(many=False)

    picture = serializers.FileField(use_url=False)

    class Meta:
        model = Event
        fields = '__all__'
