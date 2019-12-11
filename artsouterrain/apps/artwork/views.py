from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from artsouterrain.apps.artwork.models import Partner, PartnerType, Artwork, \
    ArtworkType, Place, Artist
from . import serializers


class PartnerViewSet(viewsets.ModelViewSet):

    queryset = Partner.objects.all()
    filter_fields = ('partner_type', 'partner_type__key', )
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.PartnerSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class PartnerTypeViewSet(viewsets.ModelViewSet):

    queryset = PartnerType.objects.all()
    filter_fields = '__all__'
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.PartnerTypeSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    filter_fields = '__all__'
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.ArtistSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    filter_fields = '__all__'
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.PlaceSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class ArtworkTypeViewSet(viewsets.ModelViewSet):
    queryset = ArtworkType.objects.all()
    filter_fields = '__all__'
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.ArtworkTypeSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    filter_fields = ('artist', 'place', 'artwork_type', 'level')
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.ArtworkSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
