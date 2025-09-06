import logging
from django.db import transaction
from mubaku.services.translation_service import auto_translate_instance
from apps.users.models import Profile, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mubaku.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kw):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_model(sender, instance, **kw):
    if instance:
        instance.profile.save()
        logger.info(f"{instance}'s profile was created successfully!")


@receiver(post_save, sender=Profile)
def auto_translate_profile(sender, instance, created, **kwargs):

    fields = [
        "about_me",
        "description",
    ]
    transaction.on_commit(lambda: auto_translate_instance(instance, fields))
