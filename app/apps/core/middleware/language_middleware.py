# middleware/language_middleware.py
from django.utils import translation
from django.conf import settings


class AcceptLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_languages = [lang[0] for lang in settings.LANGUAGES]

    def __call__(self, request):
        # Get language from Accept-Language header
        accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
        language_code = self._parse_accept_language(accept_language)
        print("This middlware is working...", language_code)

        # Activate the language
        translation.activate(language_code)
        request.LANGUAGE_CODE = language_code

        response = self.get_response(request)
        response["Content-Language"] = language_code
        return response

    def _parse_accept_language(self, accept_language):
        if not accept_language:
            return "en"

        # Simple parsing - you can improve this
        for lang in accept_language.split(","):
            lang = lang.split(";")[0].strip()
            if lang in self.supported_languages:
                return lang
            if lang.split("-")[0] in self.supported_languages:
                return lang.split("-")[0]

        return "en"
