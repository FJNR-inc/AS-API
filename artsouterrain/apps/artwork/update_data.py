import csv
import datetime
from io import StringIO

from artsouterrain.apps.artwork.models import UpdateData, Artist, Artwork, \
    ArtworkType, Place, PartnerType, Partner
from django.core.files.storage import default_storage

from artsouterrain.apps.event.models import Event, EventType
from artsouterrain.apps.quizz.models import Question, Page, Assessment, Choice


class UpdateDataProcess:

    places = dict()
    artwork_types = dict()
    artists = dict()
    artworks = dict()
    partner_types = dict()
    partners = dict()

    event_types = dict()
    events = dict()

    questions = dict()
    choices = dict()

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

        self.clear_event_types()
        self.create_event_types()
        self.clear_events()
        self.create_events()

        self.create_questions()
        self.create_choices()

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

    def clear_events(self):
        Event.objects.all().delete()
        self.events = dict()

    def clear_event_types(self):
        EventType.objects.all().delete()
        self.event_types = dict()

    def clear_questions(self):
        Assessment.objects.all().delete()
        Page.objects.all().delete()
        Question.objects.all().delete()
        self.questions = dict()

    def clear_choices(self):
        Choice.objects.all().delete()
        self.choices = dict()

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
                        index_itinerary=row['INDEX_ITINERARY'],
                        off_road=row['HORS_PISTE']
                    )

                if row['PHOTO']:
                    artwork.picture = row['PHOTO']
                    artwork.save()

                if row['LIEU']:
                    artwork.plan = row['LIEU']
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


    def create_event_types(self):

        f = StringIO(self.update_data.event_types_text)
        reader = csv.DictReader(f)
        for row in reader:

            if row['NOM_TYPE_EVENEMENT_FR']:

                event_type = EventType.objects.create(
                        name_fr=row['NOM_TYPE_EVENEMENT_FR'],
                        name_en=row['NOM_TYPE_EVENEMENT_EN'],
                    )

                self.event_types[row['ID_TYPE_EVENEMENT']] = event_type

    def create_events(self):

        f = StringIO(self.update_data.events_text)
        reader = csv.DictReader(f)
        for row in reader:

            if row['NOM_EVENEMENT']:

                event_date_string = row['DATE'] + ' ' + row['HEURE']
                event_date = datetime.datetime.strptime(
                    event_date_string, "%d/%m/%Y %H:%M")

                event = Event.objects.create(
                        name=row['NOM_EVENEMENT'],
                        place=self.places[
                            row['ID_LIEU']],
                        description_fr=row['DESCRIPTION_FR'],
                        description_en=row['DESCRIPTION_EN'],
                        link=row['LIEN_EVENBRITE'],
                        date=event_date,
                        event_type=self.event_types[row['ID_TYPE_EVENEMENT']],
                    )

                if row['PHOTO_EVENEMENT']:
                    event.picture = row['PHOTO_EVENEMENT']
                    event.save()

                #self.event_types[row['ID_EVENEMENT']] = event

    def create_questions(self):

        question_types = {
            'SIMPLE': 'RB',
            'MULTIPLE': 'CB'
        }

        if self.update_data.questions_text:

            self.clear_questions()

            f = StringIO(self.update_data.questions_text)
            reader = csv.DictReader(f)
            for row in reader:

                if row['QUESTION_FR']:

                    artwork = self.artworks[row['ID_OEUVRE']]
                    if artwork.assessments.count() > 1:
                        assessment = artwork.assessments.fisrt()
                    else:
                        assessment = Assessment.objects.create(
                            name=artwork.name + 'assessment',
                            artwork=artwork
                        )

                    page = Page.objects.create(
                        assessment=assessment
                    )

                    question = Question.objects.create(
                            label_fr=row['QUESTION_FR'],
                            label_en=row['QUESTION_EN'],
                            type=question_types[row['TYPE_QUESTION']],
                            page=page,
                            index=row['INDEX_QUESTION'],
                            explanation_fr=row['EXPLICATION_REPONSE_FR'],
                            explanation_en=row['EXPLICATION_REPONSE_ENG'],
                        )

                    self.questions[row['ID_QUESTIONS']] = question

    def create_choices(self):

        if self.update_data.choices_text:

            self.clear_choices()

            f = StringIO(self.update_data.choices_text)
            reader = csv.DictReader(f)
            for row in reader:

                if row['TEXTE_CHOIX_FR']:

                    Choice.objects.create(
                            label_fr=row['TEXTE_CHOIX_FR'],
                            label_en=row['TEXTE_CHOIX_EN'],
                            question=self.questions[row['ID_QUESTION']],
                            is_valid=row['VRAI_FAUX'] == 'VRAI',
                            index=row['INDEX_CHOIX'],
                        )
