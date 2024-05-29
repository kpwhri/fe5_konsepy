import pytest

from fe5_konsepy.concepts.smoking import SmokingCategory, RUN_REGEXES_FUNC


@pytest.mark.parametrize('text, exp', [
    ('positive smoking history', SmokingCategory.HISTORY),
    ('former smoker', SmokingCategory.HISTORY),
    ('quit smoking', SmokingCategory.HISTORY),
    ('packs/day: 0.25', SmokingCategory.CURRENT),
    ('pack years: 63.00', SmokingCategory.HISTORY),
    ('pack years: 0', SmokingCategory.NEVER),
    ('pack years: 0.00', SmokingCategory.NEVER),
    ('packs/day: 0', SmokingCategory.NO),
    ('packs/day: 0.0', SmokingCategory.NO),
    ('packs per day 1', SmokingCategory.CURRENT),
    ('1 pack per day', SmokingCategory.CURRENT),
    ('current smoker', SmokingCategory.CURRENT),
    ('smoking tobacco use: never', SmokingCategory.NEVER),
    ('smoking status: never', SmokingCategory.NEVER),
    ('never smoking', SmokingCategory.NEVER),
    ('smokes cigarettes', SmokingCategory.CURRENT),
    ('smoked marijuana', SmokingCategory.HISTORY),
    ('10 pack-year smoker', SmokingCategory.HISTORY),
    ('smoking status: never assessed', SmokingCategory.UNKNOWN),
    ('smoking status: never asked', SmokingCategory.UNKNOWN),
    ('smokes cigarettes?', SmokingCategory.UNKNOWN),
    ('smokes tobacco or marijuana', SmokingCategory.UNKNOWN),
    ('parent or caregiver that smokes tobacco', SmokingCategory.UNKNOWN),
])
def test_smoking_category(text, exp):
    results = set(RUN_REGEXES_FUNC(text))
    assert exp in results
