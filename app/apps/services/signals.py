from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import logging
from mubaku.services.translation_service import auto_translate_instance
from .models import ServiceCategory, Service

logger = logging.getLogger(__name__)


# ===== SERVICE CATEGORY SIGNALS =====
@receiver(pre_save, sender=ServiceCategory)
def check_service_category_fields_changed(sender, instance, **kwargs):
    """
    Track which ServiceCategory fields changed before saving
    """
    if instance.pk:
        try:
            old_instance = ServiceCategory.objects.get(pk=instance.pk)
            instance._changed_fields = []

            translatable_fields = ["name", "description"]

            for field in translatable_fields:
                old_value = getattr(old_instance, field, None)
                new_value = getattr(instance, field, None)
                if old_value != new_value and new_value:
                    instance._changed_fields.append(field)

        except ServiceCategory.DoesNotExist:
            instance._changed_fields = []


@receiver(post_save, sender=ServiceCategory)
def auto_translate_service_category(sender, instance, created, **kwargs):
    """
    Auto-translate ServiceCategory fields when created or updated
    """
    print("ServiceCategory signal triggered")

    fields_to_translate = []

    if created:
        # On creation, translate all translatable fields that have content
        fields_to_translate = ["name", "description"]
        fields_to_translate = [
            field for field in fields_to_translate if getattr(instance, field, None)
        ]

        print(f"New ServiceCategory created, translating fields: {fields_to_translate}")

    else:
        # On update, only translate fields that actually changed
        changed_fields = getattr(instance, "_changed_fields", [])
        fields_to_translate = [
            field for field in changed_fields if getattr(instance, field, None)
        ]

        print(
            f"ServiceCategory updated, changed fields: {changed_fields}, translating: {fields_to_translate}"
        )

    if fields_to_translate:
        print(f"Running translation for ServiceCategory fields: {fields_to_translate}")
        try:
            transaction.on_commit(
                lambda: auto_translate_instance(instance, fields_to_translate)
            )
            logger.info(
                f"Translation scheduled for ServiceCategory {instance.pk}, fields: {fields_to_translate}"
            )
        except Exception as e:
            logger.error(
                f"Error scheduling translation for ServiceCategory {instance.pk}: {str(e)}"
            )


# ===== SERVICE SIGNALS =====
@receiver(pre_save, sender=Service)
def check_service_fields_changed(sender, instance, **kwargs):
    """
    Track which Service fields changed before saving
    """
    if instance.pk:
        try:
            old_instance = Service.objects.get(pk=instance.pk)
            instance._changed_fields = []

            translatable_fields = ["name", "description"]

            for field in translatable_fields:
                old_value = getattr(old_instance, field, None)
                new_value = getattr(instance, field, None)
                if old_value != new_value and new_value:
                    instance._changed_fields.append(field)

        except Service.DoesNotExist:
            instance._changed_fields = []


@receiver(post_save, sender=Service)
def auto_translate_service(sender, instance, created, **kwargs):
    """
    Auto-translate Service fields when created or updated
    """
    print("Service signal triggered")

    fields_to_translate = []

    if created:
        # On creation, translate all translatable fields that have content
        fields_to_translate = ["name", "description"]
        fields_to_translate = [
            field for field in fields_to_translate if getattr(instance, field, None)
        ]

        print(f"New Service created, translating fields: {fields_to_translate}")

    else:
        # On update, only translate fields that actually changed
        changed_fields = getattr(instance, "_changed_fields", [])
        fields_to_translate = [
            field for field in changed_fields if getattr(instance, field, None)
        ]

        print(
            f"Service updated, changed fields: {changed_fields}, translating: {fields_to_translate}"
        )

    if fields_to_translate:
        print(f"Running translation for Service fields: {fields_to_translate}")
        try:
            transaction.on_commit(
                lambda: auto_translate_instance(instance, fields_to_translate)
            )
            logger.info(
                f"Translation scheduled for Service {instance.pk}, fields: {fields_to_translate}"
            )
        except Exception as e:
            logger.error(
                f"Error scheduling translation for Service {instance.pk}: {str(e)}"
            )
