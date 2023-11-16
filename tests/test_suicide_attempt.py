import pytest

from fe5_konsepy.concepts.suicide_attempt import SuicideAttemptCategory, REGEXES
from konsepy.regex import search_first_regex


@pytest.mark.parametrize('text, exp', [
    ('history of suicide attempt', SuicideAttemptCategory.YES),
    ('suicide attempt on 3/2022', SuicideAttemptCategory.YES),
    ('suicide attempt in college', SuicideAttemptCategory.YES),
    ('suicide attempt in April', SuicideAttemptCategory.YES),
    ('suicide attempt on 3 April 2022', SuicideAttemptCategory.YES),
    ('attempted suicide on 3/4', SuicideAttemptCategory.YES),
    ('attempted to kill himself in high school', SuicideAttemptCategory.YES),
    ('attempted to kill herself in jr high', SuicideAttemptCategory.YES),
    ('attempted to take her own life during university', SuicideAttemptCategory.YES),
    ('suicide attempt 1 year ago', SuicideAttemptCategory.YES),
    ('suicide attempt a year ago', SuicideAttemptCategory.YES),
    ('suicide attempt two months ago', SuicideAttemptCategory.YES),
    ('suicide attempt several years ago', SuicideAttemptCategory.YES),
    ('denies suicide attempt several years ago', SuicideAttemptCategory.NO),
    ('family history of suicide attempt', SuicideAttemptCategory.NO),
])
def test_suicide_attempt_regexes(text, exp):
    results = set(search_first_regex(REGEXES)(text))
    assert exp in results
