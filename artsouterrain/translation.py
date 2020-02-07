from modeltranslation.translator import TranslationOptions, register

from artsouterrain.apps.artwork.models import PartnerType, ArtworkMedia, \
    Artwork, ArtworkType, Place, Artist, Partner
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
        'description'
    )


@register(Artist)
class ArtistTranslationOptions(TranslationOptions):
    fields = (
        'first_name',
        'last_name',
        'country',
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


