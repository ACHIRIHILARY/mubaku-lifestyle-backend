from modeltranslation.translator import register, TranslationOptions
from .models import Notification, LoyaltyProgram


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("title", "message")


@register(LoyaltyProgram)
class LoyaltyProgramTranslationOptions(TranslationOptions):
    fields = ()  # No text fields to translate
