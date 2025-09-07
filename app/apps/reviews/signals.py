from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import logging
from mubaku.services.translation_service import auto_translate_instance
from .models import Review, Dispute

logger = logging.getLogger(__name__)


# ===== REVIEW SIGNALS =====
@receiver(pre_save, sender=Review)
def check_review_fields_changed(sender, instance, **kwargs):
    """
    Track which Review fields changed before saving
    """
    if instance.pk:
        try:
            old_instance = Review.objects.get(pk=instance.pk)
            instance._changed_fields = []

            translatable_fields = ["comment"]

            for field in translatable_fields:
                old_value = getattr(old_instance, field, None)
                new_value = getattr(instance, field, None)
                if old_value != new_value and new_value:
                    instance._changed_fields.append(field)

        except Review.DoesNotExist:
            instance._changed_fields = []


@receiver(post_save, sender=Review)
def auto_translate_review(sender, instance, created, **kwargs):
    """
    Auto-translate Review fields when created or updated
    """
    print("Review signal triggered")

    fields_to_translate = []

    if created:
        # On creation, translate if comment has content
        if instance.comment:
            fields_to_translate = ["comment"]
            print(f"New Review created, translating comment")

    else:
        # On update, only translate if comment changed and has content
        changed_fields = getattr(instance, "_changed_fields", [])
        fields_to_translate = [
            field for field in changed_fields if getattr(instance, field, None)
        ]

        print(
            f"Review updated, changed fields: {changed_fields}, translating: {fields_to_translate}"
        )

    if fields_to_translate:
        print(f"Running translation for Review fields: {fields_to_translate}")
        try:
            transaction.on_commit(
                lambda: auto_translate_instance(instance, fields_to_translate)
            )
            logger.info(
                f"Translation scheduled for Review {instance.pk}, fields: {fields_to_translate}"
            )
        except Exception as e:
            logger.error(
                f"Error scheduling translation for Review {instance.pk}: {str(e)}"
            )


# ===== DISPUTE SIGNALS =====
@receiver(pre_save, sender=Dispute)
def check_dispute_fields_changed(sender, instance, **kwargs):
    """
    Track which Dispute fields changed before saving
    """
    if instance.pk:
        try:
            old_instance = Dispute.objects.get(pk=instance.pk)
            instance._changed_fields = []

            translatable_fields = ["reason", "admin_notes"]

            for field in translatable_fields:
                old_value = getattr(old_instance, field, None)
                new_value = getattr(instance, field, None)
                if old_value != new_value and new_value:
                    instance._changed_fields.append(field)

        except Dispute.DoesNotExist:
            instance._changed_fields = []


@receiver(post_save, sender=Dispute)
def auto_translate_dispute(sender, instance, created, **kwargs):
    """
    Auto-translate Dispute fields when created or updated
    """
    print("Dispute signal triggered")

    fields_to_translate = []

    if created:
        # On creation, translate all translatable fields that have content
        fields_to_translate = ["reason"]
        if instance.admin_notes:
            fields_to_translate.append("admin_notes")

        fields_to_translate = [
            field for field in fields_to_translate if getattr(instance, field, None)
        ]
        print(f"New Dispute created, translating fields: {fields_to_translate}")

    else:
        # On update, only translate fields that actually changed
        changed_fields = getattr(instance, "_changed_fields", [])
        fields_to_translate = [
            field for field in changed_fields if getattr(instance, field, None)
        ]

        print(
            f"Dispute updated, changed fields: {changed_fields}, translating: {fields_to_translate}"
        )

    if fields_to_translate:
        print(f"Running translation for Dispute fields: {fields_to_translate}")
        try:
            transaction.on_commit(
                lambda: auto_translate_instance(instance, fields_to_translate)
            )
            logger.info(
                f"Translation scheduled for Dispute {instance.pk}, fields: {fields_to_translate}"
            )
        except Exception as e:
            logger.error(
                f"Error scheduling translation for Dispute {instance.pk}: {str(e)}"
            )
