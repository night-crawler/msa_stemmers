import typing as t
from copy import copy

import pycountry
from nltk import SnowballStemmer, LancasterStemmer
from nltk.stem import snowball

from msa_stemmers.schemas import LanguageSchema
from . import jsonrpc

STEMMER_MAP = {
    'danish': {
        'nltk.snowball': snowball.DanishStemmer,
    },
    'dutch': {
        'nltk.snowball': snowball.DutchStemmer,
    },
    'english': {
        'nltk.snowball': snowball.EnglishStemmer,
        'nltk.lancaster': LancasterStemmer,
        'nltk.porter': snowball.PorterStemmer,
    },
    'finnish': {
        'nltk.snowball': snowball.FinnishStemmer,
    },
    'french': {
        'nltk.snowball': snowball.FrenchStemmer,
    },
    'german': {
        'nltk.snowball': snowball.GermanStemmer,
    },
    'hungarian': {
        'nltk.snowball': snowball.HungarianStemmer,
    },
    'italian': {
        'nltk.snowball': snowball.ItalianStemmer,
    },
    'norwegian': {
        'nltk.snowball': snowball.NorwegianStemmer,
    },
    'portuguese': {
        'nltk.snowball': snowball.PortugueseStemmer,
    },
    'romanian': {
        'nltk.snowball': snowball.RomanianStemmer,
    },
    'russian': {
        'nltk.snowball': snowball.RussianStemmer,
    },
    'spanish': {
        'nltk.snowball': snowball.SpanishStemmer,
    },
    'swedish': {
        'nltk.snowball': snowball.SwedishStemmer,
    },
}

DEFAULT_PARSER_OPTIONS_MAP = {
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
def get_stemmer_options(stemmer_class, update_options: dict) -> dict:
    if stemmer_class not in DEFAULT_PARSER_OPTIONS_MAP:
        return update_options
    opts = copy(DEFAULT_PARSER_OPTIONS_MAP[stemmer_class])
    opts.update(update_options)
    return update_options


# на самом деле не SnowballStemmer, просто лень
def get_stemmer(lang: str, stemmer_class: str) -> t.Type[SnowballStemmer]:
    """    
    :param lang: ru | rus | russian 
    :param stemmer_class: nltk.snowball
    :return: stemmer class
    """
    if len(lang) == 2:
        lang = pycountry.languages.get(alpha_2=lang.lower())
    elif len(lang) == 3:
        lang = pycountry.languages.get(alpha_3=lang.lower())
    else:
        lang = pycountry.languages.get(name=lang.lower().capitalize())

    return STEMMER_MAP[lang.name.lower()][stemmer_class]


@jsonrpc.method('nltk.stem(String, String, String, Object) -> Array')
def stem(lang, text, stemmer_class='nltk.snowball', stemmer_options=None):
    stemmer_class = get_stemmer(lang, stemmer_class)
    stemmer_options = get_stemmer_options(stemmer_class, stemmer_options or {})
    stemmer_instance = stemmer_class(**stemmer_options)

    stemmed_words = []
    for word in text.split():
        stemmed_words.append(stemmer_instance.stem(word))

    return stemmed_words


@jsonrpc.method('nltk.stem.snowball.supported_languages() -> Array')
def supported_languages():
    res = []
    for lang, stemmers_dict in STEMMER_MAP.items():
        _lang = pycountry.languages.get(name=lang.capitalize())
        lang_bundle = LanguageSchema().dump(_lang).data
        lang_bundle['stemmers'] = []
        for stemmer_name in stemmers_dict.keys():
            lang_bundle['stemmers'].append(stemmer_name)
        res.append(lang_bundle)
    # TODO: add locale https://pypi.python.org/pypi/pycountry [Locales]
    return res