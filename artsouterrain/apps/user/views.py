from django.contrib.auth import get_user_model

from allauth.socialaccount.providers.facebook.views \
    import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.viewsets import ModelViewSet

from artsouterrain.apps.user.models import Contact
from artsouterrain.apps.user.serializers import ContactSerializer

User = get_user_model()


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    http_method_names = [u'post', u'options']
    permission_classes = ()
