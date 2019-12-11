import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from artsouterrain.apps.user.factories import AdminFactory

from ..factories import AssessmentFactory, PageFactory

from artsouterrain.apps.artwork.factories import (
    ArtworkFactory,
    ArtworkTypeFactory,
    ArtistFactory,
    PlaceFactory,
)


class PagesTests(APITestCase):

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
                assessment=self.assessments[1]
            )
        )
        self.pages[1].save()

        self.pages.append(
            PageFactory(
                assessment=self.assessments[0]
            )
        )
        self.pages[2].save()

    def test_get_list_pages(self):
        """
        Ensure we can list all pages.
        """

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(reverse('page-list'))
        self.assertEqual(json.loads(response.content)['count'], 3)

        first_page = json.loads(response.content)['results'][0]

        expected_payload = {
            'assessment': 'http://testserver' + reverse(
                "assessment-detail",
                args=[self.pages[0].assessment.id],
            ),
            'url': 'http://testserver' + reverse(
                "page-detail",
                args=[self.pages[0].id],
            ),
            'id': self.pages[0].id
        }

        self.assertEqual(first_page, expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_page(self):
        """
        Ensure that we cannot create a page
        """
        self.client.force_authenticate(user=self.admin)

        data = {'assessment': 'http://testserver' + reverse(
            "assessment-detail", args=[1])}

        response = self.client.post(
            reverse('page-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_delete_page(self):
        """
        Ensure that we cannot delete a page
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(
            reverse('page-detail', kwargs={'pk': 1}),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_update_page(self):
        """
        Ensure that we cannot update a page
        """
        self.client.force_authenticate(user=self.admin)

        data = {'assessment': 'http://testserver' + reverse(
            "assessment-detail", args=[1])}

        response = self.client.put(
            reverse('page-detail', kwargs={'pk': 1}),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_partial_update_page(self):
        """
        Ensure that we cannot partially update a page
        """
        self.client.force_authenticate(user=self.admin)

        data = {'assessment': 'http://testserver' + reverse(
            "assessment-detail", args=[1])}

        response = self.client.patch(
            reverse('page-detail', kwargs={'pk': 1}),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        expected_payload = b''
        self.assertEqual(response.content, expected_payload)

    def test_retrieve_page(self):
        """
        Ensure that we can retrieve a page
        """
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            reverse(
                'page-detail',
                kwargs={'pk': self.pages[0].id}
            ),
            format='json',
        )

        expected_payload = {
            'assessment': 'http://testserver' + reverse(
                "assessment-detail",
                args=[self.pages[0].assessment.id],
            ),
            'url': 'http://testserver' + reverse(
                "page-detail",
                args=[self.pages[0].id],
            ),
            'id': self.pages[0].id
        }

        self.assertEqual(json.loads(response.content), expected_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_page_filter_assessment(self):
        """
        Ensure that we can retrieve pages filtered by an assessment
        """
        self.client.force_authenticate(user=self.admin)

        data = {
            'assessment': self.assessments[0].id
        }

        response = self.client.get(
            reverse('page-list'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            json.loads(response.content)['count'],
            2,
        )

        first_page = json.loads(response.content)['results'][0]

        expected_payload = {
            'assessment': 'http://testserver' + reverse(
                "assessment-detail",
                args=[self.assessments[0].id],
            ),
            'url': 'http://testserver' + reverse(
                "page-detail",
                args=[self.pages[0].id],
            ),
            'id': self.pages[0].id
        }

        self.assertEqual(first_page, expected_payload)
