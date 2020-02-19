from rest_framework.routers import SimpleRouter
from django.urls import path
from django.conf.urls import include

from . import views


class OptionalSlashSimpleRouter(SimpleRouter):
    """ Subclass of SimpleRouter to make the trailing slash optional """
    def __init__(self, *args, **kwargs):
        super(SimpleRouter, self).__init__(*args, **kwargs)
        self.trailing_slash = '/?'


app_name = "artwork"

# Create a router and register our viewsets with it.
router = OptionalSlashSimpleRouter()
router.register('partner', views.PartnerViewSet)
router.register('partner_extract', views.PartnerExtractViewSet)
router.register('partner_type', views.PartnerTypeViewSet)
router.register('partner_type_extract', views.PartnerTypeExtractViewSet)
router.register('place', views.PlaceViewSet)
router.register('place_extract', views.PlaceExtractViewSet)
router.register('artist', views.ArtistViewSet)
router.register('artist_extract', views.ArtistExtractViewSet)
router.register('artwork_type', views.ArtworkTypeViewSet)
router.register('artwork_type_extract', views.ArtworkTypeExtractViewSet)
router.register('artwork', views.ArtworkViewSet)
router.register('artwork_extract', views.ArtworkExtractViewSet)
router.register('artwork_media', views.ArtworkMediaViewSet)
router.register('artwork_visit', views.ArtworkVisitViewSet)

urlpatterns = [
    path('', include(router.urls)),  # includes router generated URL
]
