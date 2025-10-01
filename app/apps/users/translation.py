from modeltranslation.translator import register, TranslationOptions
from .models import Profile, User


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = (
        "about_me",
        "description",
        "business_name",  # Added
        "business_address",  # Added
        "availability_schedule",  # Added
    )


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ()
