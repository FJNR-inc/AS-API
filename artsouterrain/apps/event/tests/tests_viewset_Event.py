import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from artsouterrain.apps.artwork.models import Place
from artsouterrain.apps.event.models import EventType, Event


class EventTexts(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.event_type = EventType.objects.create(
            key='TYPE_1',
            name='Type 1'
        )

        self.event_type_2 = EventType.objects.create(
            key='TYPE_2',
            name='Type 2'
        )

        self.place_1 = Place.objects.create(
            name='Place 1'
        )

        self.place_2 = Place.objects.create(
            name='Place 2'
        )

        self.event = Event.objects.create(
            name='Event 1',
            description='event 1 description',
            event_type=self.event_type,
            place=self.place_1,
            link='http://event2.com',
        )
        self.event_2 = Event.objects.create(
            name='Event 2',
            description='event 2 description',
            event_type=self.event_type,
            place=self.place_1,
            link='http://event2.com',
        )
        self.event_3 = Event.objects.create(
            name='Event 3',
            description='event 3 description',
            event_type=self.event_type_2,
            place=self.place_2,
            link='http://event3.com',
        )

    def test_list_event(self):

        response = self.client.get(
            reverse('event-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.content,
        )

        response_data = json.loads(response.content)

        self.assertEqual(response_data['count'], 3)

    def test_get_event(self):
        response = self.client.get(
            reverse('event-detail', kwargs={'pk': self.event.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.content,
        )

        response_data = json.loads(response.content)

        self.assertEqual(response_data['name'], self.event.name)
        self.assertEqual(response_data['link'], self.event.link)
        self.assertEqual(response_data['description'],
                         self.event.description)
        self.assertEqual(response_data['event_type']['key'],
                         self.event.event_type.key)

    def test_list_filter_by_type_key(self):
        response = self.client.get(
            reverse('event-list'),
            {'event_type__key': self.event_type.key}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.content,
        )

        response_data = json.loads(response.content)

        self.assertEqual(response_data['count'], 2)

    def test_list_filter_by_type_id(self):
        response = self.client.get(
            reverse('event-list'),
            {'event_type': self.event_type.id}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.content,
        )

        response_data = json.loads(response.content)

        self.assertEqual(response_data['count'], 2)

    def test_update_event(self):
        response = self.client.patch(
            reverse('event-detail', kwargs={'pk': self.event.id}),
            {
                'event_type': 'fake',
                'name': 'fake'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_501_NOT_IMPLEMENTED,
            response.content,
        )

    def test_delete_event(self):
        response = self.client.delete(
            reverse('event-detail', kwargs={'pk': self.event.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_501_NOT_IMPLEMENTED,
            response.content,
        )

    def test_update_event_type(self):

        response = self.client.patch(
            reverse('eventtype-detail', kwargs={'pk': self.event_type.id}),
            {
                'key': 'fake',
                'name': 'fake'
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_501_NOT_IMPLEMENTED,
            response.content,
        )

    def test_delete_event_type(self):
        response = self.client.delete(
            reverse('eventtype-detail', kwargs={'pk': self.event_type.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_501_NOT_IMPLEMENTED,
            response.content,
        )
