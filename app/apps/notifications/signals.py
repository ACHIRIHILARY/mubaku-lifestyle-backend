from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import logging
from mubaku.services.translation_service import auto_translate_instance
from .models import Notification

logger = logging.getLogger(__name__)


# ===== NOTIFICATION SIGNALS =====
@receiver(pre_save, sender=Notification)
def check_notification_fields_changed(sender, instance, **kwargs):
    """
    Track which Notification fields changed before saving
    """
    if instance.pk:
        try:
            old_instance = Notification.objects.get(pk=instance.pk)
            instance._changed_fields = []

            translatable_fields = ["title", "message"]

            for field in translatable_fields:
                old_value = getattr(old_instance, field, None)
                new_value = getattr(instance, field, None)
                if old_value != new_value and new_value:
                    instance._changed_fields.append(field)

        except Notification.DoesNotExist:
            instance._changed_fields = []


@receiver(post_save, sender=Notification)
def auto_translate_notification(sender, instance, created, **kwargs):
    """
    Auto-translate Notification fields when created or updated
    """
    print("Notification signal triggered")

    fields_to_translate = []

    if created:
        # On creation, translate all translatable fields that have content
        fields_to_translate = ["title", "message"]
        fields_to_translate = [
            field for field in fields_to_translate if getattr(instance, field, None)
        ]

        print(f"New Notification created, translating fields: {fields_to_translate}")

    else:
        # On update, only translate fields that actually changed
        changed_fields = getattr(instance, "_changed_fields", [])
        fields_to_translate = [
            field for field in changed_fields if getattr(instance, field, None)
        ]

        print(
            f"Notification updated, changed fields: {changed_fields}, translating: {fields_to_translate}"
        )

    if fields_to_translate:
        print(f"Running translation for Notification fields: {fields_to_translate}")
        try:
            transaction.on_commit(
                lambda: auto_translate_instance(instance, fields_to_translate)
            )
            logger.info(
                f"Translation scheduled for Notification {instance.pk}, fields: {fields_to_translate}"
            )
        except Exception as e:
            logger.error(
                f"Error scheduling translation for Notification {instance.pk}: {str(e)}"
            )
