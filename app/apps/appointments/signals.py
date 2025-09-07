from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import logging
from mubaku.services.translation_service import auto_translate_instance
from .models import ProviderAvailabilityException

logger = logging.getLogger(__name__)


# ===== PROVIDER AVAILABILITY EXCEPTION SIGNALS =====
@receiver(pre_save, sender=ProviderAvailabilityException)
def check_availability_exception_fields_changed(sender, instance, **kwargs):
    """
    Track which ProviderAvailabilityException fields changed before saving
    """
    if instance.pk:
        try:
            old_instance = ProviderAvailabilityException.objects.get(pk=instance.pk)
            instance._changed_fields = []

            translatable_fields = ["reason"]

            for field in translatable_fields:
                old_value = getattr(old_instance, field, None)
                new_value = getattr(instance, field, None)
                if old_value != new_value and new_value:
                    instance._changed_fields.append(field)

        except ProviderAvailabilityException.DoesNotExist:
            instance._changed_fields = []


@receiver(post_save, sender=ProviderAvailabilityException)
def auto_translate_provider_availability_exception(sender, instance, created, **kwargs):
    """
    Auto-translate ProviderAvailabilityException fields when created or updated
    """
    print("ProviderAvailabilityException signal triggered")

    fields_to_translate = []

    if created:
        # On creation, translate if reason has content
        if instance.reason:
            fields_to_translate = ["reason"]
            print(f"New ProviderAvailabilityException created, translating reason")

    else:
        # On update, only translate if reason changed and has content
        changed_fields = getattr(instance, "_changed_fields", [])
        fields_to_translate = [
            field for field in changed_fields if getattr(instance, field, None)
        ]

        print(
            f"ProviderAvailabilityException updated, changed fields: {changed_fields}, translating: {fields_to_translate}"
        )

    if fields_to_translate:
        print(
            f"Running translation for ProviderAvailabilityException fields: {fields_to_translate}"
        )
        try:
            transaction.on_commit(
                lambda: auto_translate_instance(instance, fields_to_translate)
            )
            logger.info(
                f"Translation scheduled for ProviderAvailabilityException {instance.pk}, fields: {fields_to_translate}"
            )
        except Exception as e:
            logger.error(
                f"Error scheduling translation for ProviderAvailabilityException {instance.pk}: {str(e)}"
            )
