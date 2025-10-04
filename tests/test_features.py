import pytest

from dmengine import features


@pytest.fixture(scope='session')
def fs():
    features_kwargs = [{'value': '+1', 'category': 'person'},
                       {'value': '-1', 'category': 'person'},
                       {'value': '+2', 'category': 'person'},
                       {'value': '-2', 'category': 'person'},
                       {'value': '+3', 'category': 'person'},
                       {'value': '-3', 'category': 'person'},
                       {'value': '+sg', 'category': 'number'},
                       {'value': '+pl', 'category': 'number'},
                       {'value': '-sg', 'category': 'number'},
                       {'value': '-pl', 'category': 'number'}]
    return features.FeatureSystem(features_kwargs)


def test_init(fs):
    assert [(f.value, f.category) for f in fs.FeatureSet('+1 +sg').features] == \
           [('+1', 'person'), ('+sg', 'number')]
