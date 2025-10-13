# services/translation_service.py
from deep_translator import GoogleTranslator
from django.conf import settings

def auto_translate_instance(instance, field_names):
    """
    Automatically translate an instance's fields to all supported languages
    """
    # Get the original language code from the instance if available, otherwise default to 'en'
    source_lang = getattr(instance, 'language_code', 'en')

    for lang_code, _ in settings.LANGUAGES:
        # Skip translation if the source and target languages are the same
        if lang_code == source_lang:
            continue

        print(f"Translating to {lang_code}")
        translator = GoogleTranslator(source=source_lang, target=lang_code)

        for field_name in field_names:
            # Get the original value of the field
            original_value = getattr(instance, field_name)

            if original_value:
                print(f"Translating field: {field_name}")
                
                # Translate the value
                translated_value = translator.translate(original_value)

                # Set the translated value for the specific language field
                setattr(instance, f"{field_name}_{lang_code}", translated_value)

    instance.save()