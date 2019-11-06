from rest_framework import serializers

from artsouterrain.apps.event.models import EventType, Event


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = EventType
        fields = '__all__'


class EventSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    event_type = EventTypeSerializer(many=False)

    class Meta:
        model = Event
        fields = '__all__'
