import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from artsouterrain.apps.user.factories import AdminFactory

from ..factories import AssessmentFactory, PageFactory
from ..models import Assessment, Page, Question
from ...artwork.factories import ArtworkTypeFactory, ArtistFactory, PlaceFactory, ArtworkFactory


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

        self.pages.append(
            PageFactory(
                assessment=self.assessments[0]
            )
        )
        self.pages[1].save()

        self.questions = []

        self.questions.append(Question.objects.create(
            page=self.pages[0],
            label="testQuestion", type='RB', index=0))
        self.questions[0].save()

        self.questions.append(Question.objects.create(
            page=self.pages[1],
            label="testQuestion", type='RB', index=1))
        self.questions[1].save()

        self.questions.append(Question.objects.create(
            page=self.pages[0],
            label="testQuestion", type='CB', index=2))
        self.questions[2].save()

    def test_get_list_questions(self):
        """
        Ensure we can list all questions.
        """

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(reverse('question-list'))
        self.assertEqual(json.loads(response.content)['count'], 3)

        first_question = json.loads(response.content)['results'][0]

        expected_payload = {
            'label': "testQuestion",
            'page': 'http://testserver' + reverse(
                "page-detail",
                args=[self.questions[0].page.id],
            ),
            'type': 'RB',
            'url': 'http://testserver' + reverse(
                "question-detail",
                args=[self.questions[0].id],
            ),
            'id': self.questions[0].id,
            'index': 0
        }

        self.assertEqual(first_question, expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_question(self):
        """
        Ensure that we cannot create a question
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'page': 'http://testserver' + reverse(
                "page-detail",
                args=[self.pages[0]],
            ),
            'label': "testQuestion",
            'type': 'CB',
        }

        response = self.client.post(
            reverse('question-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_delete_question(self):
        """
        Ensure that we cannot delete a question
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(
            reverse(
                'question-detail',
                kwargs={'pk': self.questions[0].id},
            ),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_update_question(self):
        """
        Ensure that we cannot update a question
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'page': 'http://testserver' + reverse(
                "page-detail",
                args=[self.questions[0].page.id],
            ),
            'label': "testQuestion2",
            'type': 'CB',
        }

        response = self.client.put(
            reverse(
                'question-detail',
                kwargs={'pk': self.questions[0].id},
            ),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_partial_update_question(self):
        """
        Ensure that we cannot partially update a question
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'page': 'http://testserver' + reverse("page-detail", args=[2]),
        }

        response = self.client.patch(
            reverse('question-detail', kwargs={'pk': 1}),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_retrieve_question(self):
        """
        Ensure that we can retrieve a question
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            reverse(
                'question-detail',
                kwargs={'pk': self.questions[0].id},
            ),
            format='json',
        )

        expected_payload = {
            'label': "testQuestion",
            'page': 'http://testserver' + reverse(
                "page-detail",
                args=[self.questions[0].page.id]
            ),
            'type': 'RB',
            'url': 'http://testserver' + reverse(
                "question-detail",
                args=[self.questions[0].id],
            ),
            'id': self.questions[0].id,
            'index': 0
        }

        self.assertEqual(json.loads(response.content), expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_question_filter_page(self):
        """
        Ensure that we can retrieve questions filtered by a page
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'page': self.pages[0].id
        }

        response = self.client.get(
            reverse('question-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json.loads(response.content)['count'], 2)

        second_question = json.loads(response.content)['results'][1]

        expected_payload = {
            'label': "testQuestion",
            'page': 'http://testserver' + reverse(
                "page-detail",
                args=[self.pages[0].id],
            ),
            'type': 'CB',
            'url': 'http://testserver' + reverse(
                "question-detail",
                args=[self.questions[2].id],
            ),
            'id': self.questions[2].id,
            'index': self.questions[2].index
        }

        self.assertEqual(second_question, expected_payload)
