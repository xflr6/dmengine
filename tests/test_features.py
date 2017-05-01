# test_features.py

import pytest

from dmengine.features import FeatureSystem


@pytest.fixture(scope='session')
def fs():
    features = [
        {'value': '+1', 'category': 'person'},
        {'value': '-1', 'category': 'person'},
        {'value': '+2', 'category': 'person'},
        {'value': '-2', 'category': 'person'},
        {'value': '+3', 'category': 'person'},
        {'value': '-3', 'category': 'person'},
        {'value': '+sg', 'category': 'number'},
        {'value': '+pl', 'category': 'number'},
        {'value': '-sg', 'category': 'number'},
        {'value': '-pl', 'category': 'number'},
    ]
    return FeatureSystem(features)


def test_init(fs):
    assert [(f.value, f.category) for f in fs.FeatureSet('+1 +sg').features] == \
           [('+1', 'person'), ('+sg', 'number')]
