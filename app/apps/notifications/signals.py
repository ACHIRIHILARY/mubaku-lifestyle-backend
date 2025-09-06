from mubaku.services.translation_service import auto_translate_instance
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Notification


@receiver(post_save, sender=Notification)
def auto_translate_notification(sender, instance, created, **kwargs):

    # Use transaction.on_commit to ensure we have a saved instance with an ID
    transaction.on_commit(
        lambda: auto_translate_instance(instance, ["title", "message"])
    )
