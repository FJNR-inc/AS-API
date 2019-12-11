from rest_framework import serializers, status

from artsouterrain.apps.user.models import Contact


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
