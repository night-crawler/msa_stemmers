from unittest.mock import patch

import nltk
import pytest
from nltk.stem.api import StemmerI
from nltk.stem.snowball import DanishStemmer

from msa_stemmers import exceptions
from msa_stemmers import utils


# noinspection PyUnusedLocal
def monkey_patched_nltk_find(resource_name, paths=None):
    raise LookupError('I AM A MOKY-MONKEY!')


# ## Should run first: mock fails after the stem() first run
# noinspection PyMethodMayBeStatic
@pytest.mark.run(order=1)
class UtilsTest:
    def test__utils__get_lang(self):
        assert utils.get_lang('ru').name == 'Russian', 'Ensure alpha-2 languages are supported'
        assert utils.get_lang('en').name == 'English', 'Ensure alpha-2 languages are supported'

        assert utils.get_lang('rus').name == 'Russian', 'Ensure alpha-3 languages are supported'
        assert utils.get_lang('eng').name == 'English', 'Ensure alpha-3 languages are supported'

        assert \
            utils.get_lang('en').name == \
            utils.get_lang('eNg').name == \
            utils.get_lang('EN').name == \
            utils.get_lang('ENGLISH').name == \
            utils.get_lang('english').name == 'English', \
            'Ensure lang is case-insensitive'

        with pytest.raises(ValueError):
            utils.get_lang('kfghl;kt')

    def test__utils__get_lang_name(self):
        assert utils.get_lang_name('ru') == 'russian'

    def test__language_stemmer_map_has_defaults(self):
        for lang_name, stemmer_name_stemmer_map in utils.LANGUAGE_STEMMERS_MAP.items():
            assert 'default' in stemmer_name_stemmer_map, 'All stemmer maps have a default'
            assert len(stemmer_name_stemmer_map) > 1, 'All stemmers map have theirs actual stemmer names'

    def test__utils__get_stemmer_class(self):
        assert issubclass(utils.get_stemmer_class('ru', 'default'), StemmerI)
        assert issubclass(utils.get_stemmer_class('en', 'default'), StemmerI)
        assert issubclass(utils.get_stemmer_class('arabic', 'default'), StemmerI)

        # raises language first
        with pytest.raises(exceptions.StemmerDoesNotExist):
            utils.get_stemmer_class('aaa', 'naa')  # pycountry/databases/iso639-3.json[0]

        with pytest.raises(exceptions.StemmerDoesNotExist):
            utils.get_stemmer_class('ru', 'naa')

    def test__utils__get_stemmer_options(self):
        from nltk import ISRIStemmer
        options = utils.get_stemmer_options(ISRIStemmer, {'new_opt': 1})
        # ISRIStemmer has no options at the moment
        assert options == {'new_opt': 1}, 'Should return the same as update_options dict if no default options present'

        options = utils.get_stemmer_options(DanishStemmer, {'new_opt': 1})
        assert 'new_opt' in options and len(options) > 1, 'Ensure merge works if default options present'

    def test__utils__ensure_nltk_ready(self):
        with pytest.raises(exceptions.NltkIsNotReady):
            with patch('nltk.data.find', monkey_patched_nltk_find):
                utils.ensure_nltk_ready()
        nltk.download('stopwords')
        utils.ensure_nltk_ready()

    def test__utils__get_stemmer(self):
        assert type(utils.get_stemmer('danish')) is DanishStemmer, 'Ensure stemmer is correct'
        assert type(utils.get_stemmer('danish', stemmer_classname='nltk.snowball')) is DanishStemmer, \
            'Ensure stemmer is correct'

        with pytest.raises(exceptions.StemmerDoesNotExist):
            utils.get_stemmer('danish', stemmer_classname='<<unknown>>')

    def test__utils__stem_text(self):
        stemmed = utils.stem_text('en', 'Go and like yourself!')
        assert stemmed == [{'Go': ['go']}, {'and': ['and']}, {'like': ['like']}, {'yourself!': ['yourself!']}]

        stemmed = utils.stem_text('en', 'Go and like yourself!', stemmer_classname='nltk.lancaster')
        assert stemmed == [{'Go': ['go']}, {'and': ['and']}, {'like': ['lik']}, {'yourself!': ['yourself!']}]

    def test__utils__activate_locale(self):
        utils.activate_locale('ru')
        assert _('English').capitalize() == 'Английский'
        utils.activate_locale('en')
        assert _('English').capitalize() == 'English'

        with pytest.raises(exceptions.LanguageDoesNotExist):
            utils.activate_locale('unknown')

        assert utils.activate_locale('unknown', silent=True) is False, 'Ensure we can suppress Exception'

        with patch('pycountry.LOCALES_DIR', '/doesnotexistklj34lj5'):
            # no locale found
            with pytest.raises(exceptions.LocaleDoesNotExist):
                utils.activate_locale('ru')

            assert utils.activate_locale('ru', silent=True) is False, 'Ensure we can suppress Exception'

        assert utils.activate_locale('ru') is True, 'Should return True if locale was installed'

    def test__utils__get_supported_languages(self):
        repr_en = None
        for stemmer_bundle in utils.get_supported_languages('ru'):
            if stemmer_bundle['name'] == 'Английский':
                repr_en = stemmer_bundle['name']
        assert repr_en == 'Английский'

        repr_en = None
        for stemmer_bundle in utils.get_supported_languages('english'):
            if stemmer_bundle['name'] == 'English':
                repr_en = stemmer_bundle['name']
        assert repr_en == 'English'

        with pytest.raises(exceptions.LanguageDoesNotExist):
            utils.get_supported_languages('unknown!', silent=False)

        assert len(utils.get_supported_languages()) == len(utils.LANGUAGE_STEMMERS_MAP)


