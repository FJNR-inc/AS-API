import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from artsouterrain.apps.user.factories import AdminFactory
from ..factories import AssessmentFactory, PageFactory
from ..models import Question, Choice
from artsouterrain.apps.artwork.factories import (
    ArtworkTypeFactory,
    ArtistFactory,
    PlaceFactory,
    ArtworkFactory,
)


class QuestionsTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = AdminFactory()
        self.admin.set_password('Test123!')
        self.admin.save()

        self.artworkType = ArtworkTypeFactory()
        self.artist = ArtistFactory()
        self.place = PlaceFactory()
        self.artwork = ArtworkFactory(
            artwork_type=self.artworkType,
            artist=self.artist,
            place=self.place,
        )

        self.assessments = []

        self.assessments.append(
            AssessmentFactory(
                artwork=self.artwork
            )
        )
        self.assessments[0].save()

        self.pages = []

        self.pages.append(
            PageFactory(
                assessment=self.assessments[0]
            )
        )
        self.pages[0].save()

        self.questions = []

        self.questions.append(Question.objects.create(
            page=self.pages[0], label="testQuestion", type='RB', index=0))
        self.questions[0].save()

        self.questions.append(Question.objects.create(
            page=self.pages[0], label="testQuestion", type='CB', index=1))
        self.questions[1].save()

        self.choices = []

        self.choices.append(Choice.objects.create(
            question=self.questions[0], label="testChoice", index=0))
        self.choices[0].save()

        self.choices.append(Choice.objects.create(
            question=self.questions[1], label="testChoice", index=0))
        self.choices[1].save()

        self.choices.append(Choice.objects.create(
            question=self.questions[0], label="testChoice", index=1))
        self.choices[2].save()

    def test_get_list_choices(self):
        """
        Ensure we can list all choices.
        """

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(reverse('choice-list'))
        self.assertEqual(json.loads(response.content)['count'], 3)

        first_choice = json.loads(response.content)['results'][0]

        expected_payload = {
            'label': "testChoice",
            'question': 'http://testserver' + reverse(
                "question-detail",
                args=[self.choices[0].question.id]
            ),
            'url': 'http://testserver' + reverse(
                "choice-detail",
                args=[self.choices[0].id],
            ),
            'id': self.choices[0].id,
            'index': 0,
            'is_valid': False,
        }

        self.assertEqual(first_choice, expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_choice(self):
        """
        Ensure that we cannot create a choice
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'question': 'http://testserver' + reverse(
                "question-detail", args=[1]),
            'label': "testChoice",
        }

        response = self.client.post(
            reverse('choice-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_delete_choice(self):
        """
        Ensure that we cannot delete a choice
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(
            reverse('choice-detail', kwargs={'pk': 1}),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_update_choice(self):
        """
        Ensure that we cannot update a choice
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'question': 'http://testserver' + reverse(
                "question-detail", args=[1]),
            'label': "testChoice",
        }

        response = self.client.put(
            reverse('choice-detail', kwargs={'pk': 1}),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_partial_update_choice(self):
        """
        Ensure that we cannot partially update a choice
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'question': 'http://testserver' + reverse(
                "question-detail", args=[2]),
        }

        response = self.client.patch(
            reverse('choice-detail', kwargs={'pk': 1}),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_retrieve_choice(self):
        """
        Ensure that we can retrieve a choice
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            reverse(
                'choice-detail',
                kwargs={'pk': self.choices[0].id}
            ),
            format='json',
        )

        expected_payload = {
            'label': "testChoice",
            'question': 'http://testserver' + reverse(
                "question-detail",
                args=[self.choices[0].question.id],
            ),
            'url': 'http://testserver' + reverse(
                "choice-detail",
                args=[self.choices[0].id]
            ),
            'id': self.choices[0].id,
            'index': 0,
            'is_valid': False,
        }

        self.assertEqual(json.loads(response.content), expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_choice_filter_question(self):
        """
        Ensure that we can retrieve choices filtered by a question
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'question': self.questions[0].id
        }

        response = self.client.get(
            reverse('choice-list'),
            data,
            format='json',
        )

        self.assertEqual(json.loads(response.content)['count'], 2)

        first_choice = json.loads(response.content)['results'][0]

        expected_payload = {
            'label': "testChoice",
            'question': 'http://testserver' + reverse(
                "question-detail",
                args=[self.questions[0].id],
            ),
            'url': 'http://testserver' + reverse(
                "choice-detail",
                args=[self.choices[0].id],
            ),
            'id': self.choices[0].id,
            'index': 0,
            'is_valid': False,
        }

        self.assertEqual(first_choice, expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
