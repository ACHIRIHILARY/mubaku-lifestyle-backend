from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from mubaku.services.translation_service import auto_translate_instance
from .models import ServiceCategory, Service


@receiver(post_save, sender=ServiceCategory)
def auto_translate_service_category(sender, instance, created, **kwargs):
    transaction.on_commit(
        lambda: auto_translate_instance(instance, ["name", "description"])
    )


@receiver(post_save, sender=Service)
def auto_translate_service(sender, instance, created, **kwargs):
    transaction.on_commit(
        lambda: auto_translate_instance(instance, ["name", "description"])
    )
