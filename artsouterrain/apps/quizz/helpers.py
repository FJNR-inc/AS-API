from django.core.exceptions import ObjectDoesNotExist

from artsouterrain.apps.quizz.models import Submission


def get_active_submission(email):
    try:
        return Submission.objects.get(
            email=email,
            completed=False
        )
    except ObjectDoesNotExist:
        return None
