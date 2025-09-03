from modeltranslation.translator import register, TranslationOptions
from .models import (
    Notification,
    LoyaltyProgram,
    Payment,
    EscrowReleaseSchedule,
    Review,
    Dispute,
)


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("title", "message")


@register(LoyaltyProgram)
class LoyaltyProgramTranslationOptions(TranslationOptions):
    fields = ()  # no translatable text fields


@register(Payment)
class PaymentTranslationOptions(TranslationOptions):
    fields = ()  # choices are handled via gettext_lazy, no free-text fields


@register(EscrowReleaseSchedule)
class EscrowReleaseScheduleTranslationOptions(TranslationOptions):
    fields = ()  # no free-text fields


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ("comment",)


@register(Dispute)
class DisputeTranslationOptions(TranslationOptions):
    fields = ("reason", "admin_notes")
