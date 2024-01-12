import random
import string

import pytest

from fe5_konsepy.concepts.suicide_attempt import SuicideAttempt, RUN_REGEXES_FUNC


def wordgen(n):
    for i in range(n):
        yield ''.join(random.choice(string.ascii_letters) for _ in range(10))


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
    ('denied history of suicide attempt', SuicideAttempt.NO),
    ('family history of suicide attempt', SuicideAttempt.NO),
    ('history of suicide attempt', SuicideAttempt.YES),
    ('history of suicide attempt: denied', SuicideAttempt.NO),
    ('suicide attempt in the past', SuicideAttempt.YES),
    ('sister had a suicide attempt in the past', SuicideAttempt.FAMILY),
    ('problem list:\n' + '\n*'.join(wordgen(5)) + '\n* history of suicide attempt', SuicideAttempt.PROBLEM_LIST),
    ('problem list\n' + '\n*'.join(wordgen(5)) + '\n* history of suicide attempt', SuicideAttempt.PROBLEM_LIST),
    ('past medical history:\n' + '\n*'.join(wordgen(5)) + '\n* history of suicide attempt',
     SuicideAttempt.PROBLEM_LIST),
    ('problem list\n' + '\n*'.join(wordgen(5)) + 'ASSESSMENT: history of suicide attempt', SuicideAttempt.YES),
    ('Z91.51', SuicideAttempt.CODE),
    ('suicide attempt a week ago per her husband', SuicideAttempt.YES),  # not FAMHX
    ('suicide attempt a week ago using mother\'s medications', SuicideAttempt.YES),  # not FAMHX
    ('suicide attempt a week ago using mother\'s pain meds', SuicideAttempt.YES),  # not FAMHX
    ('hospitalisation: denies history of suicide attempt: yes', SuicideAttempt.YES),  # not NO
    ('suicide attempt at age 15', SuicideAttempt.YES),
    ('suicide attempt in her teens', SuicideAttempt.YES),
    ('suicide attempt in his 30s', SuicideAttempt.YES),
    ('suicide attempt 3x', SuicideAttempt.YES),
    ('suicide attempt 3 times', SuicideAttempt.YES),
    ('hx of suicide attempt at cousin\'s house', SuicideAttempt.YES),
    ('hx of suicide attempt 3 times', SuicideAttempt.YES),
    ('denied hx of suicide attempt in teens', SuicideAttempt.NO),
    ('denied suicide attempt in teens', SuicideAttempt.NO),
    ('history of self-harm behavior', SuicideAttempt.YES),
    ('history of self-harm behavior: briefly', SuicideAttempt.YES),
    ('self-harm behavior: in middle school', SuicideAttempt.YES),
    ('self-harm behavior: as a student in middle school', SuicideAttempt.YES),
    ('history of deliberate self-harm', SuicideAttempt.YES),
    ('or history of deliberate self-harm', SuicideAttempt.NO),
    ('nor history of deliberate self-harm', SuicideAttempt.NO),
])
def test_suicide_attempt_regexes(text, exp):
    results = set(RUN_REGEXES_FUNC(text))
    assert exp in results
