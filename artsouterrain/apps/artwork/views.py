from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from artsouterrain.apps.artwork.models import Partner, PartnerType, Artwork, \
    ArtworkType, Place, Artist, ArtworkMedia, ArtworkVisit
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
    filter_fields = ('first_name', 'last_name', 'country' )
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
    filter_fields = ('name',)
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
        if self.action == 'list':
            return serializers.ArtworkSerializerList
        if self.action == 'retrieve':
            return serializers.ArtworkSerializerDetail
        return serializers.ArtworkSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class ArtworkMediaViewSet(viewsets.ModelViewSet):
    queryset = ArtworkMedia.objects.all()
    filter_fields = ('artwork', 'media_type',)
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.ArtworkMediaSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class ArtworkVisitViewSet(viewsets.ModelViewSet):
    queryset = ArtworkVisit.objects.all()
    filter_fields = ('artwork', 'email',)
    permission_classes = ()

    def get_serializer_class(self):
        return serializers.ArtworkMediaSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
