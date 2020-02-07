from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from .helpers import get_active_submission
from .signals import CustomAPIError


from .models import (
    Question,
    Assessment,
    Page,
    Answer,
    Choice,
    Submission,
)
from ..artwork.serializers import ArtworkSerializerHyperlink


class AssessmentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    is_completed = serializers.SerializerMethodField(read_only=True)
    number_of_questions = serializers.IntegerField(read_only=True)

    class Meta:
        model = Assessment
        fields = '__all__'

    def to_representation(self, instance):
        """Convert HyperlinkedField to NestedSerializer."""
        self.fields.pop('artwork')
        artwork = ArtworkSerializerHyperlink(many=False, read_only=True)
        self.fields['artwork'] = artwork

        return super().to_representation(instance)

    def get_is_completed(self, instance):
        if 'Email' in self.context['request'].headers.keys():
            active_submission = get_active_submission(
                self.context['request'].headers['Email'])

            if active_submission:
                questions = Question.objects.filter(page__assessment=instance)
                for question in questions:
                    contain_answer = question.answers.filter(
                        submission=active_submission
                    ).count()

                    if not contain_answer:
                        return False

                    return True

        return False


class PageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Page
        fields = '__all__'


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    choices = ChoiceSerializer(many=True)
    is_completed = serializers.SerializerMethodField(read_only=True)
    correctly_answered = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def get_correctly_answered(self, instance):
        if 'Email' in self.context['request'].headers.keys():
            active_submission = get_active_submission(
                self.context['request'].headers['Email'])

            if active_submission:
                answer = instance.answers.filter(
                    submission=active_submission).first()

                if answer:
                    return answer.is_valid

        return None

    def get_is_completed(self, instance):
        if 'Email' in self.context['request'].headers.keys():
            active_submission = get_active_submission(
                self.context['request'].headers['Email'])

            if active_submission:
                contain_answer = instance.answers.filter(
                    submission=active_submission
                ).count()

                if not contain_answer:
                    return False

                return True

        return False


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
        validators = []

    def create(self, validated_data):
        try:
            choices = validated_data.pop('choices')
            answer, created = Answer.objects.update_or_create(
                submission=validated_data['submission'],
                question=validated_data['question'],
                defaults=validated_data,
            )

            answer.choices.set(choices)

            return answer

        except CustomAPIError as e:
            raise serializers.ValidationError({
                e.code: [e.message]
            })
