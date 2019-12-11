import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from artsouterrain.apps.user.factories import AdminFactory, UserFactory

from ..factories import AssessmentFactory, PageFactory
from ..models import Question, Submission, Choice, Answer
from artsouterrain.apps.artwork.factories import (
    ArtworkTypeFactory,
    ArtistFactory,
    PlaceFactory,
    ArtworkFactory,
)


class SubmissionsTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = AdminFactory()
        self.admin.set_password('Test123!')
        self.admin.save()

        self.user = UserFactory()
        self.user.set_password('Test123!')
        self.user.save()

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

        self.assessments.append(
            AssessmentFactory(
                artwork=self.artwork
            )
        )
        self.assessments[1].save()

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

        self.pages.append(
            PageFactory(
                assessment=self.assessments[1]
            )
        )
        self.pages[2].save()

        self.question = Question.objects.create(
            page=self.pages[0],
            label="testQuestion",
            type='RB', index=0
        )

        self.question2 = Question.objects.create(
            page=self.pages[2],
            label="testQuestion2",
            type='RB', index=0,
        )

        self.choice = Choice.objects.create(
            label="testChoice",
            question=self.question, index=0,
        )

        self.choice2 = Choice.objects.create(
            label="testChoice2",
            question=self.question2,
            index=0,
        )

        self.submission = Submission.objects.create(
            user=self.admin,
        )

        self.user_submission = Submission.objects.create(
            user=self.user,
        )

        self.user_submission_completed = Submission.objects.create(
            user=self.user,
            completed=True,
        )

        self.user_submission_fully_filled = Submission.objects.create(
            user=self.user,
        )

        answer = Answer.objects.create(
            submission=self.user_submission_completed,
            question=self.question,
        )
        answer.choices.add(self.choice)
        answer.save()

        answer = Answer.objects.create(
            submission=self.user_submission_completed,
            question=self.question2,
        )
        answer.choices.add(self.choice2)
        answer.save()

        answer = Answer.objects.create(
            submission=self.user_submission_fully_filled,
            question=self.question,
        )
        answer.choices.add(self.choice)
        answer.save()

        answer = Answer.objects.create(
            submission=self.user_submission_fully_filled,
            question=self.question2,
        )
        answer.choices.add(self.choice2)
        answer.save()

    def test_get_list_submissions_as_admin(self):
        """
        Ensure we can list all submissions when we are admin.
        """

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(reverse('submission-list'))
        self.assertEqual(json.loads(response.content)['count'], 4)

        first_question = json.loads(response.content)['results'][0]

        expected_payload = {
            'created': self.submission.created.strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ),
            'updated': self.submission.updated.strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ),
            'completed': False,
            'url': 'http://testserver' + reverse(
                "submission-detail",
                args=[self.submission.id]
            ),
            'id': self.submission.id,
        }

        self.assertEqual(first_question, expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_submissions_as_user(self):
        """
        Ensure we can list all submissions when we are a simple user.
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('submission-list'))
        self.assertEqual(json.loads(response.content)['count'], 3)

        first_question = json.loads(response.content)['results'][0]

        expected_payload = {
            'created': self.user_submission.created.strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ),
            'updated': self.user_submission.updated.strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ'
            ),
            'completed': False,
            'url': 'http://testserver' + reverse(
                "submission-detail",
                args=[self.user_submission.id]
            ),
            'id': self.user_submission.id,
        }

        self.assertEqual(first_question, expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
