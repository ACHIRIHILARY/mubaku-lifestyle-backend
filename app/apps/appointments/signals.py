from mubaku.services.translation_service import auto_translate_instance
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import ProviderAvailabilityException


@receiver(post_save, sender=ProviderAvailabilityException)
def auto_translate_product(sender, instance, created, **kwargs):

    # Use transaction on_commit to ensure we have an ID
    transaction.on_commit(lambda: auto_translate_instance(instance, ["reason"]))
