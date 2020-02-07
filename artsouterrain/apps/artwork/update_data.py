import csv
from io import StringIO

from artsouterrain.apps.artwork.models import UpdateData, Artist, Artwork, \
    ArtworkType, Place
from django.core.files.storage import default_storage


class UpdateDataProcess:

    places = dict()
    artwork_types = dict()
    artists = dict()
    artworks = dict()

    def __init__(self, update_data: UpdateData):
        self.update_data = update_data

    def run(self):
        self.clear_places()
        self.create_places()
        print(self.places)
        self.clear_artwork_types()
        self.create_artwork_types()
        print(self.artwork_types)
        self.clear_artists()
        self.create_artists()
        print(self.artists)
        self.clear_artworks()
        self.create_artworks()
        print(self.artworks)
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

    def create_places(self):
        f = StringIO(self.update_data.places_text)
        reader = csv.DictReader(f)

        for row in reader:
            if row['Nom_Lieu']:
                self.places[row['ID_Lieu']] = Place.objects.create(
                    name_fr=row['Nom_Lieu'])

    def create_artwork_types(self):

        f = StringIO(self.update_data.artwork_types_text)
        reader = csv.DictReader(f)

        for row in reader:

            if row['Nom_Type_oeuvre']:
                self.artwork_types[row['ID_Type_Oeuvre']] = \
                    ArtworkType.objects.create(
                        name_fr=row['Nom_Type_oeuvre'])

    def create_artists(self):

        f = StringIO(self.update_data.artists_text)
        reader = csv.DictReader(f)

        for row in reader:

            if row['Nom']:
                new_artist = Artist.objects.create(
                        first_name_fr=row['Nom'],
                        last_name_fr=row['Prenom'],
                        country_fr=row['Pays'],)
                if row['Photo']:
                    new_artist.picture = row['Photo']
                    new_artist.save()

                self.artists[row['ID Artiste']] = new_artist

    def create_artworks(self):

        f = StringIO(self.update_data.artworks_text)
        reader = csv.DictReader(f)
        for row in reader:

            if row['Nom']:
                self.artworks[row['ID_Oeuvre']] = \
                    Artwork.objects.create(
                        name_fr=row['Nom'],
                        artist=self.artists[row['ID artist']],
                        place=self.places[row['ID lieu']],
                        description_fr=row['Description_fr'],
                        description_en=row['Description_eng'],
                        artwork_type=self.artwork_types[
                            row['ID type oeuvre']],)