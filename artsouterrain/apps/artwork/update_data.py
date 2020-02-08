import csv
from io import StringIO

from artsouterrain.apps.artwork.models import UpdateData, Artist, Artwork, \
    ArtworkType, Place, PartnerType, Partner
from django.core.files.storage import default_storage


class UpdateDataProcess:

    places = dict()
    artwork_types = dict()
    artists = dict()
    artworks = dict()
    partner_types = dict()
    partners = dict()

    def __init__(self, update_data: UpdateData):
        self.update_data = update_data

    def run(self):
        self.clear_places()
        self.create_places()

        self.clear_artwork_types()
        self.create_artwork_types()

        self.clear_artists()
        self.create_artists()

        self.clear_artworks()
        self.create_artworks()

        self.clear_partner_types()
        self.create_partner_types()

        self.clear_partners()
        self.create_partners()

    def clear_places(self):
        Place.objects.all().delete()
        self.places = dict()

    def clear_artwork_types(self):
        ArtworkType.objects.all().delete()
        self.artwork_types = dict()

    def clear_artists(self):
        Artist.objects.all().delete()
        self.artists = dict()

    def clear_artworks(self):
        Artwork.objects.all().delete()
        self.artworks = dict()

    def clear_partner_types(self):
        PartnerType.objects.all().delete()
        self.partner_types = dict()

    def clear_partners(self):
        Partner.objects.all().delete()
        self.partners = dict()

    def create_places(self):
        f = StringIO(self.update_data.places_text)
        reader = csv.DictReader(f)

        for row in reader:
            if row['NOM_LIEU_FR']:
                place = Place.objects.create(
                    name_fr=row['NOM_LIEU_FR'],
                    name_en=row['NOM_LIEU_EN'],
                )

                if row['PLAN']:
                    place.plan = row['PLAN']
                    place.save()
                self.places[row['ID_LIEU']] = place

    def create_artwork_types(self):

        f = StringIO(self.update_data.artwork_types_text)
        reader = csv.DictReader(f)

        for row in reader:

            if row['NOM_TYPE_OEUVRE_FR']:
                artwork_type = ArtworkType.objects.create(
                     name_fr=row['NOM_TYPE_OEUVRE_FR'],
                     name_en=row['NOM_TYPE_OEUVRE_EN'],
                )

                self.artwork_types[row['ID_TYPE_OEUVRE']] = artwork_type

    def create_artists(self):

        f = StringIO(self.update_data.artists_text)
        reader = csv.DictReader(f)

        for row in reader:

            if row['NOM']:
                new_artist = Artist.objects.create(
                        first_name=row['NOM'],
                        last_name=row['PRENOM'],
                        country_fr=row['PAYS_FR'],
                        country_en=row['PAYS_EN'],
                        bio_fr=row['BIO_FR'],
                        bio_en=row['BIO_EN'])
                if row['PHOTO']:
                    new_artist.picture = row['PHOTO']
                    new_artist.save()

                self.artists[row['ID_ARTISTE']] = new_artist

    def create_artworks(self):

        f = StringIO(self.update_data.artworks_text)
        reader = csv.DictReader(f)
        for row in reader:

            if row['NOM_FR']:

                artwork = Artwork.objects.create(
                        name_fr=row['NOM_FR'],
                        name_en=row['NOM_EN'],
                        artwork_type=self.artwork_types[
                            row['ID_TYPE_OEUVRE']],
                        artist=self.artists[row['ID_ARTIST']],
                        place=self.places[row['ID_LIEU']],
                        level=row['ETAGE'],
                        latitude=row['LATITUDE'],
                        longitude=row['LONGITUDE'],
                        creation_year=row['ANNEE_DE_CREATION'],
                        description_fr=row['DESCRIPTION_FR'],
                        description_en=row['DESCRIPTION_EN'],
                        index_itinerary=row['INDEX_ITINERARY']
                    )

                if row['PHOTO']:
                    artwork.picture = row['PHOTO']
                    artwork.save()

                if row['PLAN']:
                    artwork.plan = row['PLAN']
                    artwork.save()

                self.artworks[row['ID_OEUVRE']] = artwork

    def create_partner_types(self):

        f = StringIO(self.update_data.partner_type_text)
        reader = csv.DictReader(f)
        for row in reader:

            if row['NOM_PARTENAIRE_FR']:

                partner_type = PartnerType.objects.create(
                    key=row['CLEF_UNIQUE'],
                    name_fr=row['NOM_PARTENAIRE_FR'],
                    name_en=row['NOM_PARTENAIRE_EN'],
                )

                self.partner_types[row['ID_TYPE_PARTENAIRE']] = partner_type

    def create_partners(self):

        f = StringIO(self.update_data.partner_text)
        reader = csv.DictReader(f)
        for row in reader:

            if row['ID_PARTENAIRES']:

                partner = Partner.objects.create(
                    name_fr=row['NOM_FR'],
                    name_en=row['NOM_EN'],
                    partner_type=self.partner_types[row['ID_TYPE_PARTENAIRE']],
                    link_fr=row['WEBSITE_FR'],
                    link_en=row['WEBSITE_EN'],
                    description_fr=row['DESCRIPTION_FR'],
                    description_en=row['DESCRIPTION_EN'],
                )
                if row['LOGO']:
                    partner.logo = row['LOGO']
                    partner.save()

                self.partners[row['ID_PARTENAIRES']] = partner
