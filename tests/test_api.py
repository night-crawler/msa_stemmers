import pytest
import json
from uuid import uuid4


def mk_task_bundle(method_name: str, *params) -> dict:
    bundle = {
        'id': str(uuid4()),
        'jsonrpc': '2.0',
        'method': method_name,
        'params': list(params),
    }
    return json.dumps(bundle)


# noinspection PyMethodMayBeStatic
@pytest.mark.run(order=2)
class ApiTest:
    def test_supported_languages(self, client):
        localized_result = client.post('/api', data=mk_task_bundle(
            'nltk.stem.supported_languages', 'ru'
        )).json['result']
        repr_en = None
        for stemmer_bundle in localized_result:
            if stemmer_bundle['name'] == 'Английский':
                repr_en = stemmer_bundle['name']
        assert repr_en == 'Английский'

        # =========
        localized_result = client.post('/api', data=mk_task_bundle(
            'nltk.stem.supported_languages', 'en'
        )).json['result']
        repr_en = None
        for stemmer_bundle in localized_result:
            if stemmer_bundle['name'] == 'English':
                repr_en = stemmer_bundle['name']
        assert repr_en == 'English'

    def test_stemming(self, client):
        stemmed = client.post('/api', data=mk_task_bundle(
            'nltk.stem', 'en', 'Go and like yourself!'
        )).json['result']
        assert stemmed == [{'Go': ['go']}, {'and': ['and']}, {'like': ['like']}, {'yourself!': ['yourself!']}]

        stemmed = client.post('/api', data=mk_task_bundle(
            'nltk.stem', 'en', 'Go and like yourself!', 'nltk.lancaster', {'strip_prefix_flag': True}
        )).json['result']
        assert stemmed == [{'Go': ['go']}, {'and': ['and']}, {'like': ['lik']}, {'yourself!': ['yourself!']}]
