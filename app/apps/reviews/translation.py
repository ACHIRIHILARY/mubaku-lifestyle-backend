from modeltranslation.translator import register, TranslationOptions
from .models import (
    Review,
    Dispute,
)


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ("comment",)


@register(Dispute)
class DisputeTranslationOptions(TranslationOptions):
    fields = ("reason", "admin_notes")
