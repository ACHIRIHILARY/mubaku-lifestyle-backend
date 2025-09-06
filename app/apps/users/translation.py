from modeltranslation.translator import register, TranslationOptions
from .models import Profile, User


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = (
        "about_me",
        "address",
        "business_name",
        "business_address",
        "description",
        "city",
    )


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = (
        "first_name",
        "last_name",
        "username",
    )
