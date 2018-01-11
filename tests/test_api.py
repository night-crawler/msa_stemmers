import pytest


# noinspection PyMethodMayBeStatic
class ApiTest:
    @pytest.mark.options(debug=False)
    def test_app(self, app):
        assert not app.debug, 'Ensure the app not in debug mode'

    def test_supported_languages(self, server):
        repr_en = None
        for stemmer_bundle in server.nltk.stem.supported_languages('ru')['result']:
            if stemmer_bundle['name'] == 'Английский':
                repr_en = stemmer_bundle['name']
        assert repr_en == 'Английский'

        repr_en = None
        for stemmer_bundle in server.nltk.stem.supported_languages('english')['result']:
            if stemmer_bundle['name'] == 'English':
                repr_en = stemmer_bundle['name']
        assert repr_en == 'English'

    def test_stemming(self, server):
        stemmed = server.nltk.stem('en', 'Go and like yourself!')['result']
        assert stemmed == [{'Go': ['go']}, {'and': ['and']}, {'like': ['like']}, {'yourself!': ['yourself!']}]

        stemmed = server.nltk.stem(
            'en', 'Go and like yourself!', 'nltk.lancaster', {'strip_prefix_flag': True}
        )['result']
        assert stemmed == [{'Go': ['go']}, {'and': ['and']}, {'like': ['lik']}, {'yourself!': ['yourself!']}]
