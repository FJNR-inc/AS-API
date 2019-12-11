from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _

from artsouterrain.apps.quizz.models import Submission


class User(AbstractUser):
    """Abstraction of the base User model. Needed to extend in the future."""

    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def active_submission(self):
        try:
            return Submission.objects.get(
                user=self,
                completed=False
            )
        except ObjectDoesNotExist:
            return None
