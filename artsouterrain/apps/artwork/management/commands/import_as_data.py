import csv

from django.core.management.base import BaseCommand

from artsouterrain.apps.artwork.models import Place, ArtworkType, Artist, \
    Artwork


class Command(BaseCommand):
    help = 'Clean and create data'

    places_file_name = 'import_data/place.csv'
    artwork_types_file_name = 'import_data/artwork_type.csv'
    artists_file_name = 'import_data/artists.csv'
    artworks_file_name = 'import_data/artwork.csv'

    places = dict()
    artwork_types = dict()
    artists = dict()
    artworks = dict()

    def handle(self, *args, **options):
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
        with open(self.places_file_name) as place_file:

            reader = csv.DictReader(place_file)

            for row in reader:
                if row['Nom_Lieu']:
                    self.places[row['ID_Lieu']] = Place.objects.create(
                        name_fr=row['Nom_Lieu'])

    def create_artwork_types(self):
        with open(self.artwork_types_file_name) as artwork_types:
            reader = csv.DictReader(artwork_types)

            for row in reader:

                if row['Nom_Type_oeuvre']:
                    self.artwork_types[row['ID_Type_Oeuvre']] = \
                        ArtworkType.objects.create(
                            name_fr=row['Nom_Type_oeuvre'])

    def create_artists(self):
        with open(self.artists_file_name) as artists:
            reader = csv.DictReader(artists)

            for row in reader:

                if row['Nom']:
                    self.artists[row['ID Artiste']] = \
                        Artist.objects.create(
                            first_name_fr=row['Nom'],
                            last_name_fr=row['Prenom'],
                            country_fr=row['Pays'],)

    def create_artworks(self):
        with open(self.artworks_file_name) as artworks:
            reader = csv.DictReader(artworks)

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






