from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from mubaku.services.translation_service import auto_translate_instance
from .models import Review, Dispute


@receiver(post_save, sender=Review)
def auto_translate_review(sender, instance, created, **kwargs):
    if created and instance.comment:
        transaction.on_commit(lambda: auto_translate_instance(instance, ["comment"]))


@receiver(post_save, sender=Dispute)
def auto_translate_dispute(sender, instance, created, **kwargs):
    if created:
        fields_to_translate = ["reason"]
        if instance.admin_notes:
            fields_to_translate.append("admin_notes")

        transaction.on_commit(
            lambda: auto_translate_instance(instance, fields_to_translate)
        )
