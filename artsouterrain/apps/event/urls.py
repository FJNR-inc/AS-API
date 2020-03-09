from rest_framework.routers import SimpleRouter
from django.urls import path
from django.conf.urls import include

from . import views


class OptionalSlashSimpleRouter(SimpleRouter):
    """ Subclass of SimpleRouter to make the trailing slash optional """
    def __init__(self, *args, **kwargs):
        super(SimpleRouter, self).__init__(*args, **kwargs)
        self.trailing_slash = '/?'


app_name = "event"

router = OptionalSlashSimpleRouter()
router.register('event', views.EventViewSet)
router.register('event_extract', views.EventExtractViewSet)
router.register('event_type', views.EventTypeViewSet)
router.register('event_type_extract', views.EventTypeExtractViewSet)

urlpatterns = [
    path('', include(router.urls)),  # includes router generated URL
]
