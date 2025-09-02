from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from mubaku.services.translation_service import auto_translate_instance
from .models import Payment


@receiver(post_save, sender=Payment)
def auto_translate_payment(sender, instance, created, **kwargs):
    if created:
        # Translate escrow_release_trigger if provided
        transaction.on_commit(
            lambda: auto_translate_instance(instance, ["escrow_release_trigger"])
        )
