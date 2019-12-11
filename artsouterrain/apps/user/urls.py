
from django.urls import path
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from artsouterrain.apps.user.views import FacebookLogin
from . import views


class OptionalSlashDefaultRouter(DefaultRouter):
    """ Subclass of DefaultRouter to make the trailing slash optional """

    def __init__(self, *args, **kwargs):
        super(DefaultRouter, self).__init__(*args, **kwargs)
        self.trailing_slash = '/?'


# Create a router and register our viewsets with it.
router = OptionalSlashDefaultRouter()

router.register('contact', views.ContactViewSet)

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^accounts/', include('allauth.urls'), name='socialaccount_signup'),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    path('', include(router.urls)),  # includes router generated URL
]
