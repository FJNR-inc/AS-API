from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from artsouterrain.apps.artwork.models import Partner, PartnerType, Artist, \
    Place, ArtworkType, Artwork, ArtworkMedia, ArtworkVisit, UpdateData

admin.site.register(Partner)
admin.site.register(PartnerType)
admin.site.register(Artist)
admin.site.register(Place)
admin.site.register(ArtworkType)


@admin.register(Artwork)
class ArtworkAdmin(TranslationAdmin):
    list_display = (
        'id',
        'name',
        'artist',
        'place',
        'artwork_type',
        'qr_code_token'
    )

    list_filter = (
        'artist',
        'place',
        'artwork_type'
    )

    fieldsets = (
        (
            None, {
                'fields': (
                    'name',
                    'artist',
                    'place',
                    'description',
                    'picture',
                    'artwork_type',
                    'level',
                    'latitude',
                    'longitude',
                    'qr_code_token',
                    'plan',
                    'index_itinerary',
                    'next_artwork',
                    'previous_artwork',
                )
            }
         ),
    )

    readonly_fields = (
        'qr_code_token', 'next_artwork', 'previous_artwork',
    )


@admin.register(ArtworkMedia)
class ArtworkMediaAdmin(TranslationAdmin):
    list_display = (
        'id',
        'artwork',
        'name',
        'media_type'
    )

    list_filter = (
        'artwork',
        'media_type',
    )


@admin.register(ArtworkVisit)
class ArtworkVisitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'artwork',
        'email',
        'visit_date'
    )

    list_filter = (
        'artwork',
        'email',
        'visit_date'
    )


def update_data(modeladmin, request, queryset):
    for data in queryset.all():
        data.update_data()


update_data.short_description = "Upload data"


@admin.register(UpdateData)
class UpdateDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'create_date',
    )

    list_filter = (
        'create_date',
    )

    actions = (update_data,)
