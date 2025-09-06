from modeltranslation.translator import register, TranslationOptions
from .models import Profile, User


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = (
        "about_me",
        "description",
    )


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ()
