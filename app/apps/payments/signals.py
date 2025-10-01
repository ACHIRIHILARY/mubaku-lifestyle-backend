from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import logging
from mubaku.services.translation_service import auto_translate_instance
from .models import Payment

logger = logging.getLogger(__name__)


# ===== PAYMENT SIGNALS =====
@receiver(pre_save, sender=Payment)
def check_payment_fields_changed(sender, instance, **kwargs):
    """
    Track which Payment fields changed before saving
    """
    if instance.pk:
        try:
            old_instance = Payment.objects.get(pk=instance.pk)
            instance._changed_fields = []

            translatable_fields = ["escrow_release_trigger"]

            for field in translatable_fields:
                old_value = getattr(old_instance, field, None)
                new_value = getattr(instance, field, None)
                if old_value != new_value and new_value:
                    instance._changed_fields.append(field)

        except Payment.DoesNotExist:
            instance._changed_fields = []


@receiver(post_save, sender=Payment)
def auto_translate_payment(sender, instance, created, **kwargs):
    """
    Auto-translate Payment fields when created or updated
    """
    print("Payment signal triggered")

    fields_to_translate = []

    if created:
        # On creation, translate if escrow_release_trigger has content
        if instance.escrow_release_trigger:
            fields_to_translate = ["escrow_release_trigger"]
            print(f"New Payment created, translating escrow_release_trigger")

    else:
        # On update, only translate if escrow_release_trigger changed and has content
        changed_fields = getattr(instance, "_changed_fields", [])
        fields_to_translate = [
            field for field in changed_fields if getattr(instance, field, None)
        ]

        print(
            f"Payment updated, changed fields: {changed_fields}, translating: {fields_to_translate}"
        )

    if fields_to_translate:
        print(f"Running translation for Payment fields: {fields_to_translate}")
        try:
            transaction.on_commit(
                lambda: auto_translate_instance(instance, fields_to_translate)
            )
            logger.info(
                f"Translation scheduled for Payment {instance.pk}, fields: {fields_to_translate}"
            )
        except Exception as e:
            logger.error(
                f"Error scheduling translation for Payment {instance.pk}: {str(e)}"
            )
