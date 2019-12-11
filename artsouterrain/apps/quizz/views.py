from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.reverse import reverse

from .signals import CustomAPIError
from .models import *
from . import serializers


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    filter_fields = '__all__'

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
    filter_fields = {'label', 'type', 'page'}

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
    filter_fields = {'user', 'completed'}
    serializer_class = serializers.SubmissionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Submission.objects.all()
        else:
            return Submission.objects.filter(user=self.request.user)

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
        submission = self.request.user.active_submission
        if not submission:
            submission = Submission.objects.create(
                user=self.request.user
            )

        request.data['submission'] = reverse(
            'submission-detail',
            args=[submission.id],
            request=request
        )

        response = super().create(request)
        return response
