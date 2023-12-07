import pytest

from fe5_konsepy.concepts.suicide_attempt import SuicideAttempt, RUN_REGEXES_FUNC


@pytest.mark.parametrize('text, exp', [
    ('history of suicide attempt', SuicideAttempt.YES),
    ('suicide attempt on 3/2022', SuicideAttempt.YES),
    ('suicide attempt in college', SuicideAttempt.YES),
    ('suicide attempt in April', SuicideAttempt.YES),
    ('suicide attempt on 3 April 2022', SuicideAttempt.YES),
    ('attempted suicide on 3/4', SuicideAttempt.YES),
    ('attempted to kill himself in high school', SuicideAttempt.YES),
    ('attempted to kill herself in jr high', SuicideAttempt.YES),
    ('attempted to take her own life during university', SuicideAttempt.YES),
    ('suicide attempt 1 year ago', SuicideAttempt.YES),
    ('suicide attempt a year ago', SuicideAttempt.YES),
    ('suicide attempt two months ago', SuicideAttempt.YES),
    ('suicide attempt several years ago', SuicideAttempt.YES),
    ('denies suicide attempt several years ago', SuicideAttempt.NO),
    ('family history of suicide attempt', SuicideAttempt.NO),
    ('history of suicide attempt', SuicideAttempt.YES),
    ('history of suicide attempt: denied', SuicideAttempt.NO),
    ('suicide attempt in the past', SuicideAttempt.YES),
    ('sister had a suicide attempt in the past', SuicideAttempt.FAMILY),
])
def test_suicide_attempt_regexes(text, exp):
    results = set(RUN_REGEXES_FUNC(text))
    assert exp in results
