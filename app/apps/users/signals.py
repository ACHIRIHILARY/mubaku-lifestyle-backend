import logging

from apps.users.models import Profile
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
