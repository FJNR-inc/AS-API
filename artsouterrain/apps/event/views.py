from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from artsouterrain.apps.artwork.models import Partner, PartnerType, Artwork, \
    ArtworkType, Place, Artist
from artsouterrain.apps.event.models import Event, EventType
from . import serializers


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    filter_fields = ('event_type', 'event_type__key', )
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.EventSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class EventTypeViewSet(viewsets.ModelViewSet):

    queryset = EventType.objects.all()
    filter_fields = '__all__'
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.EventTypeSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
