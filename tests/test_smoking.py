import pytest

from fe5_konsepy.concepts.smoking import SmokingCategory, RUN_REGEXES_FUNC


@pytest.mark.parametrize('text, exp', [
    ('positive smoking history', SmokingCategory.HISTORY),
    ('former smoker', SmokingCategory.HISTORY),
    ('quit smoking', SmokingCategory.HISTORY),
    ('packs/day: 0.25', SmokingCategory.HISTORY),
    ('pack years: 63.00', SmokingCategory.HISTORY),
    ('packs/day: 0', SmokingCategory.NO),
    ('packs per day 1', SmokingCategory.HISTORY),
    ('1 pack per day', SmokingCategory.HISTORY),
    ('current smoker', SmokingCategory.CURRENT),
    ('smoking tobacco use: never', SmokingCategory.NEVER),
    ('smoking status: never', SmokingCategory.NEVER),
    ('never smoking', SmokingCategory.NEVER),
    ('smokes cigarettes', SmokingCategory.CURRENT),
    ('smoked marijuana', SmokingCategory.HISTORY),
    ('10 pack-year smoker', SmokingCategory.HISTORY),

])
def test_suicide_attempt_regexes(text, exp):
    results = set(RUN_REGEXES_FUNC(text))
    assert exp in results
