import gettext
import os
import typing as t
from copy import copy

import pycountry
from nltk import LancasterStemmer, ISRIStemmer
from nltk.stem import snowball
from nltk.stem.api import StemmerI

from msa_stemmers import exceptions
from msa_stemmers.schemas import LanguageSchema

LANGUAGE_STEMMERS_MAP = {
    'danish': {
        'default': snowball.DanishStemmer,
        'nltk.snowball': snowball.DanishStemmer,
    },
    'dutch': {
        'default': snowball.DutchStemmer,
        'nltk.snowball': snowball.DutchStemmer,
    },
    'english': {
        'default': snowball.EnglishStemmer,
        'nltk.snowball': snowball.EnglishStemmer,
        'nltk.lancaster': LancasterStemmer,
        'nltk.porter': snowball.PorterStemmer,
    },
    'finnish': {
        'default': snowball.FinnishStemmer,
        'nltk.snowball': snowball.FinnishStemmer,
    },
    'french': {
        'default': snowball.FrenchStemmer,
        'nltk.snowball': snowball.FrenchStemmer,
    },
    'german': {
        'default': snowball.GermanStemmer,
        'nltk.snowball': snowball.GermanStemmer,
    },
    'hungarian': {
        'default': snowball.HungarianStemmer,
        'nltk.snowball': snowball.HungarianStemmer,
    },
    'italian': {
        'default': snowball.ItalianStemmer,
        'nltk.snowball': snowball.ItalianStemmer,
    },
    'norwegian': {
        'default': snowball.NorwegianStemmer,
        'nltk.snowball': snowball.NorwegianStemmer,
    },
    'portuguese': {
        'default': snowball.PortugueseStemmer,
        'nltk.snowball': snowball.PortugueseStemmer,
    },
    'romanian': {
        'default': snowball.RomanianStemmer,
        'nltk.snowball': snowball.RomanianStemmer,
    },
    'russian': {
        'default': snowball.RussianStemmer,
        'nltk.snowball': snowball.RussianStemmer,
    },
    'spanish': {
        'default': snowball.SpanishStemmer,
        'nltk.snowball': snowball.SpanishStemmer,
    },
    'swedish': {
        'default': snowball.SwedishStemmer,
        'nltk.snowball': snowball.SwedishStemmer,
    },
    'arabic': {
        'default': ISRIStemmer,  # takes no args
        'nltk.isri': ISRIStemmer,
    }
}

DEFAULT_STEMMER_OPTIONS_MAP = {
    snowball.DanishStemmer: {'ignore_stopwords': True},
    snowball.DutchStemmer: {'ignore_stopwords': True},
    snowball.EnglishStemmer: {'ignore_stopwords': True},
    snowball.FinnishStemmer: {'ignore_stopwords': True},
    snowball.FrenchStemmer: {'ignore_stopwords': True},
    snowball.GermanStemmer: {'ignore_stopwords': True},
    snowball.HungarianStemmer: {'ignore_stopwords': True},
    snowball.ItalianStemmer: {'ignore_stopwords': True},
    snowball.NorwegianStemmer: {'ignore_stopwords': True},
    snowball.PorterStemmer: {'ignore_stopwords': True},
    snowball.PortugueseStemmer: {'ignore_stopwords': True},
    snowball.RomanianStemmer: {'ignore_stopwords': True},
    snowball.RussianStemmer: {'ignore_stopwords': True},
    snowball.SpanishStemmer: {'ignore_stopwords': True},
    snowball.SwedishStemmer: {'ignore_stopwords': True},
}


# на данный момент оно не понимает args, но имхо это и не нужно
def get_stemmer_options(stemmer_class: t.Type[StemmerI], update_options: dict) -> dict:
    """
    Merges default stemmer options from DEFAULT_STEMMER_OPTIONS_MAP with update_options
    :param stemmer_class: stemmer class, may be a subclass of StemmerI
    :param update_options: a dict with new options
    :return: combined options dict
    """
    if stemmer_class not in DEFAULT_STEMMER_OPTIONS_MAP:
        return update_options
    opts = copy(DEFAULT_STEMMER_OPTIONS_MAP[stemmer_class])
    opts.update(update_options)
    return opts


def get_lang(lang: str) -> 'pycountry.db.Data':
    """
    :param lang: 'ru' | 'rus' | 'russian'
    :return: instance of pycountry.db.Data
    >>> get_lang('en')
    >>> Language(alpha_2='en', alpha_3='eng', name='English', scope='I', type='L')
    """
    try:
        if len(lang) == 2:
            return pycountry.languages.get(alpha_2=lang.lower())
        elif len(lang) == 3:
            return pycountry.languages.get(alpha_3=lang.lower())
        else:
            return pycountry.languages.get(name=lang.lower().capitalize())
    except KeyError:
        pass

    raise exceptions.LanguageDoesNotExist('Unknown language: %s' % lang)


def get_lang_name(lang: str) -> str:
    """
    Returns lowercase full language name
    :param lang: 'ru' | 'rus' | 'russian'
    :return: instance of str like 'russian'
    """
    return get_lang(lang).name.lower()


# на самом деле не SnowballStemmer, просто лень
def get_stemmer_class(lang: str, stemmer_classname: str) -> t.Type[StemmerI]:
    """
    :param lang: 'ru' | 'rus' | 'russian'
    :param stemmer_classname: 'nltk.snowball' | 'default'
    :return: stemmer class
    """
    lang_name = get_lang_name(lang)

    stemmers = LANGUAGE_STEMMERS_MAP.get(lang_name)
    if not stemmers:
        raise exceptions.StemmerDoesNotExist(
            'No stemmer for language {0}({1})'.format(lang, lang_name))

    stemmer_class = stemmers.get(stemmer_classname)
    if not stemmer_class:
        raise exceptions.StemmerDoesNotExist(
            'No stemmer with classname {0}'.format(stemmer_classname))

    return stemmer_class


def get_stemmer(lang, stemmer_classname='default', **stemmer_options) -> StemmerI:
    """
    Creates an instance of stemmer class with additional `stemmer_options`
     merged with hardcoded default options. At the moment there's nothing
     acceptable except 'ignore_stopwords'.
    :param lang: 'ru' | 'rus' | 'russian'
    :param stemmer_classname: 'default' | 'nltk.snowball'
    :param stemmer_options: a dict with options
    :return:
    """
    stemmer_class = get_stemmer_class(lang, stemmer_classname)
    stemmer_options = get_stemmer_options(stemmer_class, stemmer_options or {})
    return stemmer_class(**stemmer_options)


def ensure_nltk_ready():
    """
    Checks if stopwords are downloaded. Hides to noisy exceptions from nltk.
    """
    try:
        get_stemmer('danish')
    except LookupError:
        raise exceptions.NltkIsNotReady("Run `nltk.download('stopwords')`!")


def stem_text(lang: str, text: str,
              stemmer_classname: str = 'default',
              **stemmer_options) -> t.List[t.Dict[str, t.List[str]]]:
    """
    Performs stemming of preliminarily cleaned (by you) text.
    Special chars are not being processed as you wish.
    >>> stem_text('en', 'Go and like yourself!', stemmer_classname='nltk.lancaster')
    >>> [{'Go': ['go']}, {'and': ['and']}, {'like': ['lik']}, {'yourself!': ['yourself!']}]

    :param lang: 'ru' | 'rus' | 'russian'
    :param text: a string with text to stem; text should be cleaned of special chars
    :param stemmer_classname: 'default' | 'nltk.snowball' | 'etc...'
    :param stemmer_options: a dict with options
    :return: a list of mappings {<word>: [<stem_candidate1>, ...]}
    """
    stemmer = get_stemmer(lang, stemmer_classname, **stemmer_options)
    stemmed_words = []
    for word in text.split():
        stemmed_words.append({word: [stemmer.stem(word)]})

    return stemmed_words


def activate_locale(language_or_language_code: str, silent: bool = False):
    """
    Activate all locales under LC_MESSAGES, for example:
        iso639-3.mo
        iso639_3.mo
        iso3166.mo
        iso3166-1.mo
        iso3166-3.mo
        iso4217.mo
        iso15924.mo

    :param language_or_language_code: 'ru' | 'rus' | 'russian'
    :param silent: suppress exceptions
    :return: True if there were no exceptions, False otherwise (if silent == True).
    """
    try:
        lang = get_lang(language_or_language_code)
    except exceptions.LanguageDoesNotExist:
        if silent:
            return False
        else:
            raise

    lang_code = lang.alpha_2

    locale_dir = os.path.join(pycountry.LOCALES_DIR, lang_code, 'LC_MESSAGES')
    if not os.path.exists(locale_dir):
        lang_code = lang.alpha_3
        locale_dir = os.path.join(pycountry.LOCALES_DIR, lang_code, 'LC_MESSAGES')

        if not os.path.exists(locale_dir):
            if silent:
                return False
            raise exceptions.LocaleDoesNotExist(
                'Cannot find a locale for language %s' % language_or_language_code)

    initial_translation = None
    for locale_filename in os.listdir(locale_dir):
        if not os.path.isfile(os.path.join(locale_dir, locale_filename)):
            continue
        domain = os.path.splitext(locale_filename)[0]
        translation = gettext.translation(domain, pycountry.LOCALES_DIR, languages=[lang_code])
        if not initial_translation:
            initial_translation = translation
        else:
            initial_translation.add_fallback(translation)
    initial_translation and initial_translation.install()
    return True


# _translation = None
# for locale_filename in os.listdir(locale_dir):
#     if not os.path.isfile(os.path.join(locale_dir, locale_filename)):
#         continue
#     domain = os.path.splitext(locale_filename)[0]
#     translation = gettext.translation(domain, pycountry.LOCALES_DIR, languages=[lang_code])
#     if not _translation:
#         _translation = translation
#     else:
#         _translation.add_fallback(translation)
#     print('install', translation, domain)
# _translation and _translation.install()


def get_supported_languages(language: str = 'en', silent=True):
    """
    :param language: 'ru' | 'rus' | 'russian'
    :param silent: suppress activate_locale exceptions
    :return: list of language bundles

    >>> get_supported_languages()
    >>> [
    >>>     {
    >>>         'name': 'Danish', 'type': 'L', 'alpha_2': 'da', 'scope': 'I', 'alpha_3': 'dan',
    >>>         'stemmers': ['default', 'nltk.snowball']
    >>>     },
    >>>     ...
    >>> ]
    """
    activate_locale(language, silent=silent)

    res = []
    for lang, stemmers_dict in LANGUAGE_STEMMERS_MAP.items():
        _lang = pycountry.languages.get(name=lang.capitalize())
        lang_bundle = LanguageSchema().dump(_lang).data
        lang_bundle['stemmers'] = []
        for stemmer_name in stemmers_dict:
            lang_bundle['stemmers'].append(stemmer_name)
        res.append(lang_bundle)
    return res
