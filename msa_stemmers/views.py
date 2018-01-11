from msa_stemmers import jsonrpc
from msa_stemmers.utils import stem_text, get_supported_languages


@jsonrpc.method('nltk.stem(String, String, String, Object) -> Array')
def stem(lang, text, stemmer_classname='default', stemmer_options=None):
    stemmer_options = stemmer_options or {}
    return stem_text(lang, text, stemmer_classname=stemmer_classname, **stemmer_options)


@jsonrpc.method('nltk.stem.supported_languages(String, Boolean) -> Array')
def supported_languages(language='en', silent=True):
    return get_supported_languages(language, silent=silent)
