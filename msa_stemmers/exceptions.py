class StemmerDoesNotExist(ValueError):
    pass


class LanguageDoesNotExist(ValueError):
    pass


class NltkIsNotReady(LookupError):
    pass


class LocaleDoesNotExist(ValueError):
    pass
