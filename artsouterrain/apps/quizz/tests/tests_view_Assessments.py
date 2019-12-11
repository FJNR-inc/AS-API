import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from artsouterrain.apps.user.factories import AdminFactory
from ..models import (
    Assessment,
    Page,
    Question,
    Choice,
    Submission,
    Answer,
)
from artsouterrain.apps.artwork.models import (
    Artwork,
    ArtworkType,
    Place,
    Artist,
)


class AssessmentsTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = AdminFactory()
        self.admin.set_password('Test123!')
        self.admin.save()

        self.artwork_type = ArtworkType.objects.create(
            name='Type 1',
        )

        self.place = Place.objects.create(
            name='place 1',
        )

        self.artist = Artist.objects.create(
            first_name='artist 1',
        )

        self.artwork = Artwork.objects.create(
            name='art 1',
            artist=self.artist,
            place=self.place,
            artwork_type=self.artwork_type,
        )

        self.assessment = Assessment.objects.create(
            artwork=self.artwork,
            name="testAssessment",
        )

        self.assessment2 = Assessment.objects.create(
            artwork=self.artwork,
            name="testAssessment2",
        )

        self.page = Page.objects.create(
            assessment=self.assessment2,
        )

        self.question = Question.objects.create(
            label='Question 1',
            type='RB',
            page=self.page,
            index=0,
        )

        self.page2 = Page.objects.create(
            assessment=self.assessment,
        )

        self.question2 = Question.objects.create(
            label='Question 1',
            type='RB',
            page=self.page2,
            index=0,
        )

        self.choice = Choice.objects.create(
            question=self.question2,
            label='testChoice',
            index=0,
        )

        self.submission = Submission.objects.create(
            user=self.admin,
        )

        self.answer = Answer.objects.create(
            question=self.question2,
            submission=self.submission,
        )

        self.answer.choices.add(self.choice)
        self.answer.save()

    def test_get_list_assessments(self):
        """
        Ensure we can list all assessments.
        """

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            reverse('assessment-list')
        )
        self.assertEqual(
            json.loads(response.content)['count'],
            2
        )

        first_assessment = json.loads(response.content)['results'][0]

        expected_payload = {
            'artwork': 'http://testserver' + reverse(
                "artwork-detail",
                args=[self.assessment.artwork.id],
            ),
            'name': self.assessment.name,
            'url': 'http://testserver' + reverse(
                "assessment-detail",
                args=[self.assessment.id],
            ),
            'is_completed': True,
            'information_text': None,
            'id': self.assessment.id,
            'number_of_questions': 1,
        }

        self.assertEqual(first_assessment, expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_assessment(self):
        """
        Ensure that we cannot create an assessment
        """
        self.client.force_authenticate(user=self.admin)

        data = {'name': 'TestAssessment'}

        response = self.client.post(
            reverse('assessment-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_delete_assessment(self):
        """
        Ensure that we cannot delete an assessment
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(
            reverse('assessment-detail', kwargs={'pk': 1}),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_update_assessment(self):
        """
        Ensure that we cannot update an assessment
        """
        self.client.force_authenticate(user=self.admin)

        data = {'name': 'TestAssessment2'}

        response = self.client.put(
            reverse('assessment-detail', kwargs={'pk': 1}),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_partial_update_assessment(self):
        """
        Ensure that we cannot partially update an assessment
        """
        self.client.force_authenticate(user=self.admin)

        data = {'name': 'TestAssessment2'}

        response = self.client.patch(
            reverse('assessment-detail', kwargs={'pk': 1}),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_retrieve_assessment_completed(self):
        """
        Ensure that we can retrieve an assessment
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            reverse('assessment-detail', kwargs={'pk': self.assessment.pk}),
            format='json',
        )

        expected_payload = {
            'artwork': 'http://testserver' + reverse(
                "artwork-detail",
                args=[self.assessment.artwork.id]
            ),
            'name': self.assessment.name,
            'url': 'http://testserver' + reverse(
                "assessment-detail",
                args=[self.assessment.id]
            ),
            'is_completed': True,
            'id': self.assessment.id,
            'information_text': None,
            'number_of_questions': 1,
        }

        self.assertEqual(json.loads(response.content), expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_assessment_uncompleted(self):
        """
        Ensure that we can retrieve an assessment uncompleted
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            reverse('assessment-detail',
                    kwargs={'pk': self.assessment2.pk}),
            format='json',
        )

        expected_payload = {
            'artwork': 'http://testserver' + reverse(
                "artwork-detail",
                args=[self.assessment2.artwork.id]
            ),
            'name': self.assessment2.name,
            'url': 'http://testserver' + reverse(
                "assessment-detail",
                args=[self.assessment2.id]
            ),
            'is_completed': False,
            'id': self.assessment2.id,
            'information_text': None,
            'number_of_questions': 1,
        }

        self.assertEqual(json.loads(response.content), expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
