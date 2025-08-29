# services/translation_service.py
from googletrans import Translator
from django.conf import settings

translator = Translator()


def auto_translate_instance(instance, field_names):
    """
    Automatically translate an instance's fields to all supported languages
    """
    for lang_code, _ in settings.LANGUAGES:

        for field_name in field_names:

            # get the value of the field
            value = getattr(instance, field_name)

            # get the translated value
            translated_value = translator.translate(value, dest=lang_code).text

            # set the translated value
            setattr(instance, f"{field_name}_{lang_code}", translated_value)

    instance.save()
