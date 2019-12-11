from django.db import models
from django.utils.translation import ugettext_lazy as _


class Assessment(models.Model):
    name = models.CharField(
        max_length=200,
    )

    information_text = models.TextField(
        null=True,
        blank=True,
    )

    artwork = models.ForeignKey(
        'artwork.Artwork',
        on_delete=models.CASCADE,
        related_name='assessments',
    )

    def __str__(self):
        return self.name

    @property
    def number_of_questions(self):
        return Question.objects.filter(
            page__assessment=self
        ).count()


class Page(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='pages',
    )

    def __str__(self):
        return str(self.assessment) + ", " + str(self.id)


class Question(models.Model):

    QUESTION_TYPE = (
        ('RB', 'RadioButton'),
        ('CB', 'CheckBox')
    )

    label = models.CharField(
        max_length=400,
    )

    type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE,
    )

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    index = models.PositiveIntegerField(
        verbose_name=_("Index of the question")
    )

    explanation = models.TextField(
        verbose_name=_("Explanation of the answer"),
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('index',)

    def __str__(self):
        return self.label


class Choice(models.Model):
    label = models.CharField(
        max_length=400,
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )

    # Define is the choice is the good choice or not
    # ---
    # If is_valid is True, the choice should be selected as
    # an answer to the question
    is_valid = models.BooleanField(
        default=False,
    )

    index = models.PositiveIntegerField(
        verbose_name=_("Index of the choice")
    )

    class Meta:
        ordering = ('index',)

    def __str__(self):
        return self.label


class Submission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    email = models.CharField(
        max_length=255,
        verbose_name=_("Participant email")
    )
    completed = models.BooleanField(default=False)


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    choices = models.ManyToManyField(
        Choice,
        blank=True,
    )

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("question", "submission"),)

    @property
    def is_valid(self):
        valid_choices = self.question.choices.filter(is_valid=True).count()
        valid_choices_selected = Choice.objects.filter(is_valid=True, answer=self).count()

        return valid_choices == valid_choices_selected
