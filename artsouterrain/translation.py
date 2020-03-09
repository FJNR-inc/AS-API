from modeltranslation.translator import TranslationOptions, register

from artsouterrain.apps.artwork.models import PartnerType, ArtworkMedia, \
    Artwork, ArtworkType, Place, Artist, Partner
from artsouterrain.apps.event.models import EventType, Event
from artsouterrain.apps.quizz.models import Choice, Question, Assessment


@register(PartnerType)
class PartnerTypeTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(Partner)
class PartnerTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'link'
    )


@register(Artist)
class ArtistTranslationOptions(TranslationOptions):
    fields = (
        'country',
        'bio'
    )


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(ArtworkType)
class ArtworkTypeTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(Artwork)
class ArtworkTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )


@register(ArtworkMedia)
class ArtworkMediaTranslationOptions(TranslationOptions):
    fields = (
        'detail',
    )


@register(Assessment)
class AssessmentTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'information_text',
    )


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = (
        'label',
        'explanation',
    )


@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = (
        'label',
    )


@register(EventType)
class EventTypeTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = (
        'description',
    )




