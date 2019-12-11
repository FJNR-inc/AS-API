from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.reverse import reverse

from .helpers import get_active_submission
from .signals import CustomAPIError
from .models import *
from . import serializers


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    filter_fields = '__all__'
    permission_classes = ()

    serializer_class = serializers.AssessmentSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    filter_fields = '__all__'
    permission_classes = ()

    serializer_class = serializers.PageSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    filter_fields = {'label', 'type', 'page', 'page__assessment'}
    permission_classes = ()

    serializer_class = serializers.QuestionSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    filter_fields = {'label', 'question'}
    permission_classes = ()

    serializer_class = serializers.ChoiceSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    filter_fields = {'email', 'completed'}
    serializer_class = serializers.SubmissionSerializer
    permission_classes = ()

    def get_queryset(self):
        if 'Email' in self.request.headers.keys():
            return Submission.objects.filter(email=self.request.headers['Email'])
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    filter_fields = '__all__'
    permission_classes = ()

    serializer_class = serializers.AnswerSerializer

    def get_queryset(self):
        user = str(self.request.user.id)
        asked_user = self.request.query_params.get('user', None)
        if asked_user is not None and asked_user != user:
            raise CustomAPIError(
                'One user cannot get answers from another user',
                code='user',
            )
        return Answer.objects.filter(submission__user_id=user)

    def create(self, request,  *args, **kwargs):
        submission = get_active_submission(self.request.headers['Email'])
        if not submission:
            submission = Submission.objects.create(
                email=self.request.headers['Email']
            )

        request.data['submission'] = reverse(
            'submission-detail',
            args=[submission.id],
            request=request
        )

        response = super().create(request)
        return response
