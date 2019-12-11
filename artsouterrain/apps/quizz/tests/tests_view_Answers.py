import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from artsouterrain.apps.user.factories import AdminFactory, UserFactory
from ..factories import AssessmentFactory, PageFactory
from ..helpers import get_active_submission
from ..models import Assessment, Page, Question, Submission, Choice
from ...artwork.factories import ArtworkTypeFactory, ArtistFactory, PlaceFactory, ArtworkFactory


class AnswersTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = AdminFactory()
        self.admin.set_password('Test123!')
        self.admin.save()

        self.user = UserFactory()
        self.user.set_password('Test123!')
        self.user.save()

        self.user_without_submission = UserFactory()
        self.user_without_submission.set_password('Test123!')
        self.user_without_submission.save()

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

        self.question = Question.objects.create(
            page=self.pages[0],
            label="testQuestion",
            type='RB', index=0
        )

        self.question2 = Question.objects.create(
            page=self.pages[0],
            label="testQuestion2",
            type='RB', index=1
        )

        self.choice = Choice.objects.create(
            label="testChoice",
            question=self.question, index=0
        )

        self.choice2 = Choice.objects.create(
            label="testChoice2",
            question=self.question2, index=1
        )

        self.submission = Submission.objects.create(
            email="admin@fjnr.ca",
        )

        self.user_submission = Submission.objects.create(
            email="user@fjnr.ca",
        )

    def test_create_answer(self):
        """
        Ensure that we can create a new answer
        """
        self.client.credentials(HTTP_EMAIL='user@fjnr.ca')

        data = {
            'question': 'http://testserver' + reverse(
                "question-detail",
                args=[self.question.id]
            ),
            'choices': [
                'http://testserver' + reverse(
                    "choice-detail",
                    args=[self.choice.id]
                ),
            ]
        }

        response = self.client.post(
            reverse('answer-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_payload = {
            'submission': 'http://testserver' + reverse(
                "submission-detail",
                args=[self.user_submission.id]
            ),
            'question': 'http://testserver' + reverse(
                "question-detail",
                args=[self.question.id]
            ),
            'choices': [
                'http://testserver' + reverse(
                    "choice-detail",
                    args=[self.choice.id]
                ),
            ],
            'url': 'http://testserver' + reverse(
                "answer-detail",
                args=[1]
            ),
            'id': 1,
        }
        self.assertEqual(json.loads(response.content), expected_payload)

    def test_create_answer_without_submission(self):
        """
        Ensure that we can create a new answer without having a submission
        active
        """
        self.client.credentials(HTTP_EMAIL='user.without.submission@fjnr.ca')

        data = {
            'question': 'http://testserver' + reverse(
                "question-detail",
                args=[self.question.id]
            ),
            'choices': [
                'http://testserver' + reverse(
                    "choice-detail",
                    args=[self.choice.id]
                ),
            ]
        }

        response = self.client.post(
            reverse('answer-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_payload = {
            'submission': 'http://testserver' + reverse(
                "submission-detail",
                args=[get_active_submission('user.without.submission@fjnr.ca').id]
            ),
            'question': 'http://testserver' + reverse(
                "question-detail",
                args=[self.question.id]
            ),
            'choices': [
                'http://testserver' + reverse(
                    "choice-detail",
                    args=[self.choice.id]
                ),
            ],
            'url': 'http://testserver' + reverse(
                "answer-detail",
                args=[1]
            ),
            'id': 1,
        }
        self.assertEqual(json.loads(response.content), expected_payload)

    def test_create_answer_with_non_coherent_choices(self):
        """
        Ensure that we can't create a new answer with non coherent choices
        ie: One of the choice is not related to the question we answer
        """

        self.client.credentials(HTTP_EMAIL='user.without.submission@fjnr.ca')

        data = {
            'question': 'http://testserver' + reverse(
                "question-detail",
                args=[self.question.id]
            ),
            'choices': [
                'http://testserver' + reverse(
                    "choice-detail",
                    args=[self.choice2.id]
                ),
            ]
        }

        response = self.client.post(
            reverse('answer-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_payload = {
            'choices': [
                'choices must refer to the question of the answer'
            ]
        }
        self.assertEqual(json.loads(response.content), expected_payload)
