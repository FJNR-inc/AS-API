from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .signals import CustomAPIError


from .models import (
    Question,
    Assessment,
    Page,
    Answer,
    Choice,
    Submission,
)


class AssessmentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    is_completed = serializers.SerializerMethodField(read_only=True)
    number_of_questions = serializers.IntegerField(read_only=True)

    class Meta:
        model = Assessment
        fields = '__all__'

    def get_is_completed(self, instance):
        questions = Question.objects.filter(page__assessment=instance)
        for question in questions:
            contain_answer = question.answers.filter(
                submission=self.context['request'].user.active_submission
            ).count()

            if not contain_answer:
                return False

        return True


class PageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Page
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = '__all__'


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Choice
        fields = '__all__'


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Submission
        fields = [
            'id',
            'url',
            'created',
            'updated',
            'completed',
        ]


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except CustomAPIError as e:
            raise serializers.ValidationError({
                e.code: [e.message]
            })
