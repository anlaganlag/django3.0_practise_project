
from django.conf import settings
from django.db import models
from django.utils.translation import get_language
from django.utils import translation




class TranslatedField(object):
    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, instance, owner):
        lang_code = translation.get_language()
        if lang_code == settings.LANGUAGE_CODE:
            return getattr(instance, self.field_name)
        else:
            translations = instance.translations.filter(
                language=lang_code,
            ).first() or instance
            