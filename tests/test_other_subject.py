import pytest

from fe5_konsepy.other_subject import OTHER_SUBJECT_RX, has_other_subject


@pytest.mark.parametrize('text, exp', [
    ('sister', True),
])
def test_other_subject(text, exp):
    assert bool(OTHER_SUBJECT_RX.search(text)) == exp


@pytest.mark.parametrize('text, exp', [
    ('sister', 'sister'),
    ('patient', None),
])
def test_other_subject_func(text, exp):
    assert has_other_subject(text) == exp
