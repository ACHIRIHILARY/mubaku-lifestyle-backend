import logging
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from mubaku.services.translation_service import auto_translate_instance
from apps.users.models import Profile, User
from mubaku.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update user profile when User instance is saved
    """
    try:
        if created:
            # Create new profile for new user
            Profile.objects.create(user=instance)
            logger.info(f"Profile created for user: {instance.username}")
        else:
            # Ensure profile exists and save it
            if hasattr(instance, "profile"):
                instance.profile.save()
                logger.debug(f"Profile saved for user: {instance.username}")
    except Exception as e:
        logger.error(
            f"Error in create_or_update_user_profile for {instance.username}: {str(e)}"
        )


@receiver(pre_save, sender=Profile)
def check_profile_fields_changed(sender, instance, **kwargs):
    """
    Track which fields changed before saving to determine if translation is needed
    """
    if instance.pk:
        try:
            old_instance = Profile.objects.get(pk=instance.pk)
            instance._changed_fields = []

            # Check which translatable fields have changed - UPDATED WITH NEW FIELDS
            translatable_fields = [
                "about_me",
                "description",
                "business_name",
                "business_address",
                "availability_schedule",
            ]

            for field in translatable_fields:
                old_value = getattr(old_instance, field, None)
                new_value = getattr(instance, field, None)
                # Only translate if field changed AND has non-empty content
                if old_value != new_value and new_value and str(new_value).strip():
                    instance._changed_fields.append(field)

        except Profile.DoesNotExist:
            instance._changed_fields = []


@receiver(post_save, sender=Profile)
def auto_translate_profile(sender, instance, created, **kwargs):
    """
    Auto-translate profile fields when created or specific fields are updated
    """
    print("Profile signal triggered")

    fields_to_translate = []

    # Define all translatable fields - UPDATED WITH NEW FIELDS
    translatable_fields = [
        "about_me",
        "description",
        "business_name",
        "business_address",
        "availability_schedule",
    ]

    if created:
        # On creation, translate all translatable fields that have content
        fields_to_translate = [
            field
            for field in translatable_fields
            if getattr(instance, field, None) and str(getattr(instance, field)).strip()
        ]

        print(f"New profile created, translating fields: {fields_to_translate}")

    else:
        # On update, only translate fields that actually changed
        changed_fields = getattr(instance, "_changed_fields", [])
        fields_to_translate = [
            field
            for field in changed_fields
            if getattr(instance, field, None) and str(getattr(instance, field)).strip()
        ]

        print(
            f"Profile updated, changed fields: {changed_fields}, translating: {fields_to_translate}"
        )

    # Only proceed if there are fields to translate
    if fields_to_translate:
        print(f"Running translation for fields: {fields_to_translate}")
        try:
            # Use transaction.on_commit to ensure translation happens after successful save
            transaction.on_commit(
                lambda: auto_translate_instance(instance, fields_to_translate)
            )
            logger.info(
                f"Translation scheduled for profile {instance.pk}, fields: {fields_to_translate}"
            )
        except Exception as e:
            logger.error(
                f"Error scheduling translation for profile {instance.pk}: {str(e)}"
            )
    else:
        print("No fields need translation")


@receiver(post_save, sender=User)
def update_user_related_fields(sender, instance, created, **kwargs):
    """
    Update related fields when User instance is saved
    """
    if not created and hasattr(instance, "profile"):
        try:
            profile = instance.profile
            update_needed = False

            # Sync phone number if it's different (based on your requirement to keep both)
            if instance.phone_number != profile.phone_number:
                profile.phone_number = instance.phone_number
                update_needed = True

            # Save profile only if changes were made
            if update_needed:
                profile.save()
                logger.debug(f"Synced user fields to profile for: {instance.username}")

        except Exception as e:
            logger.error(
                f"Error updating user related fields for {instance.username}: {str(e)}"
            )


# New signal for provider application - auto-translate business details
@receiver(post_save, sender=Profile)
def auto_translate_provider_application(sender, instance, created, **kwargs):
    """
    Auto-translate provider business details when application is submitted
    This runs separately from the main translation to handle provider-specific fields
    """
    # Only process if this is a provider profile with business details
    if (
        instance.user.role == "provider"
        and instance.provider_application_status == "pending"
        and any(
            [instance.business_name, instance.description, instance.business_address]
        )
    ):

        provider_fields_to_translate = []

        # Check which provider fields have content
        if instance.business_name and str(instance.business_name).strip():
            provider_fields_to_translate.append("business_name")
        if instance.description and str(instance.description).strip():
            provider_fields_to_translate.append("description")
        if instance.business_address and str(instance.business_address).strip():
            provider_fields_to_translate.append("business_address")
        if (
            instance.availability_schedule
            and str(instance.availability_schedule).strip()
        ):
            provider_fields_to_translate.append("availability_schedule")

        if provider_fields_to_translate:
            print(
                f"Translating provider business fields: {provider_fields_to_translate}"
            )
            try:
                transaction.on_commit(
                    lambda: auto_translate_instance(
                        instance, provider_fields_to_translate
                    )
                )
                logger.info(
                    f"Provider business translation scheduled for profile {instance.pk}, "
                    f"fields: {provider_fields_to_translate}"
                )
            except Exception as e:
                logger.error(
                    f"Error scheduling provider business translation for profile {instance.pk}: {str(e)}"
                )
