import factory

from artsouterrain.apps.quizz.models import Assessment, Page


class AssessmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Assessment

    name = factory.Sequence('assessment{0}'.format)

    @classmethod
    def __init__(self, **kwargs):
        kwargs.pop('artwork', None)

        assessment = super(AssessmentFactory, self).__init__(self, **kwargs)
        assessment.save()


class PageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Page

    @classmethod
    def __init__(self, **kwargs):
        kwargs.pop('page', None)

        page = super(PageFactory, self).__init__(self, **kwargs)
        page.save()
