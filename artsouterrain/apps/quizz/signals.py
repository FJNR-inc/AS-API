from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from .models import Answer
from django.core.exceptions import ValidationError


class CustomAPIError(ValidationError):
    pass


@receiver(m2m_changed, sender=Answer.choices.through)
def my_handler(sender, instance, **kwargs):
    ok = True
    if instance.choices.all():
        for choice in instance.choices.all():
            if choice.question != instance.question:
                ok = False
    if not ok:
        raise CustomAPIError(
            'choices must refer to the question of the answer',
            code='choices'
        )