import enum
import re

from konsepy.regex import search_all_regex

from fe5_konsepy.other_subject import has_other_subject


class SmokingCategory(enum.Enum):
    """Start from 1; each must be distinct; use CAPITAL_LETTERS_WITH_UNDERSCORE is possible"""
    UNKNOWN = -1
    NO = 0
    CURRENT = 1
    HISTORY = 2
    NEVER = 3
    YES = 4
    FAMILY = 5


history = '(?:history|hx)'
smoking_history = fr'(?:positive|given|significant|year|for)\W*smoking\W*{history}'
smoker = r'(?:smoker)'
former = r'(?:former|past|previous)'
current = r'(?:current)'
no_longer = r'(?:quit|no\W*longer|stopped)'
smoking = r'(?:smok(?:es|ing))'
packs_per_day = r'(?:packs?/day|packs?\W*per\W*day)'
pack_years = r'(?:pack\W*years?)'
digit = r'(?:\d+(?:\.\d+)?)'
smoking_status = r'(?:smoking|tobacco)\W*(?:use|usage|status)'
never = r'(?:never|no(?:ne)?)'
smoke_target = r'(?:marijuana|tobacco|cigarettes?|cigars?)'
curr_smokes = r'(?:smokes)'
past_smoked = r'(?:smoked|used to smoke)'


def check_if_zero(default_value=SmokingCategory.HISTORY):
    def _check_if_zero(m, text):
        val = float(m.group('num'))
        if val:
            return default_value
        return None

    return _check_if_zero


def check_if_after(n_chars, regex, newcategory):
    def _check_if_after(m, text):
        text = text[m.end(): m.end() + n_chars]
        if regex.search(text):
            return newcategory
        return None

    return _check_if_after


def check_if_before(n_chars, regex, newcategory):
    def _check_if_before(m, text):
        text = text[max(0, m.start() - n_chars): m.start()]
        if regex.search(text):
            return newcategory
        return None

    return _check_if_before


def has_other_subject_before(newcategory):
    def _has_other_subject_before(m, text):
        text = text[max(0, m.start() - 20): m.start()]
        if has_other_subject(text):
            return newcategory
        return None

    return _has_other_subject_before


def check_sentence_is_question(newcategory):
    def _check_sentence_is_question(m, text):
        for letter in text[m.end():]:
            if letter in {';', '.', '!'}:
                return None
            elif letter in {'?'}:
                return newcategory

    return _check_sentence_is_question


def check_if_hypothetical():
    pre_func = check_if_before(20, re.compile(r'\bor\b', re.I), SmokingCategory.UNKNOWN)
    post_func = check_if_after(20, re.compile(r'\bor\b', re.I), SmokingCategory.UNKNOWN)
    question_func = check_sentence_is_question(SmokingCategory.UNKNOWN)
    other_subject_func = has_other_subject_before(SmokingCategory.FAMILY)
    funcs = [pre_func, post_func, question_func, other_subject_func]

    def _check_if_hypothetical(m, text):
        for func in funcs:
            if cat := func(m, text):
                return cat
        return None

    return _check_if_hypothetical


REGEXES = [
    (re.compile(rf'\b{smoking_history}\b', re.I), SmokingCategory.HISTORY),
    (re.compile(rf'\b{former}\W*{smoker}\b', re.I), SmokingCategory.HISTORY,
     has_other_subject_before(SmokingCategory.FAMILY),
     ),
    (re.compile(rf'\b{no_longer}\W*{smoking}\b', re.I), SmokingCategory.HISTORY,
     has_other_subject_before(SmokingCategory.FAMILY),
     ),
    (re.compile(rf'\bnever\W*{smoking}\b', re.I), SmokingCategory.NEVER),
    (re.compile(rf'\b{current}\W*{smoker}\b', re.I), SmokingCategory.CURRENT,
     has_other_subject_before(SmokingCategory.FAMILY),
     ),
    (re.compile(rf'\b{packs_per_day}\W*(?P<num>{digit})\b', re.I), SmokingCategory.NO,
     check_if_zero(SmokingCategory.CURRENT)
     ),
    (re.compile(rf'\b{pack_years}\W*(?P<num>{digit})\b', re.I), SmokingCategory.NEVER,
     check_if_zero()
     ),
    (re.compile(rf'\b(?P<num>{digit})\W*{packs_per_day}\b', re.I), SmokingCategory.NO,
     check_if_zero(SmokingCategory.CURRENT)
     ),
    (re.compile(rf'\b(?P<num>{digit})\W*{pack_years}\b', re.I), SmokingCategory.NEVER,
     check_if_zero()
     ),
    (re.compile(rf'\b{smoking_status}\W*{never}\b', re.I), SmokingCategory.NEVER,
     check_if_after(20, re.compile(r'(?:assessed|asked)', re.I), SmokingCategory.UNKNOWN)
     ),
    (re.compile(rf'\b{smoking_status}\W*(?:{former})\b', re.I), SmokingCategory.HISTORY),
    (re.compile(rf'\b{smoking_status}\W*(?:{current})\b', re.I), SmokingCategory.CURRENT),
    (re.compile(rf'\b{curr_smokes}\W*{smoke_target}\b', re.I), SmokingCategory.CURRENT,
     check_if_hypothetical(),
     ),
    (re.compile(rf'\b{past_smoked}\W*{smoke_target}\b', re.I), SmokingCategory.HISTORY,
     check_if_hypothetical(),
     ),
]


def search_all_regex_func(regexes):
    """For each regex, return all, but run 3rd argument if a function (use finditer)"""

    def _search_all_regex(text, include_match=False):
        for regex, category, *other in regexes:
            func = None
            if len(other) > 0:
                func = other[0]
            for m in regex.finditer(text):
                if func and (res := func(m, text)):
                    yield (res, m) if include_match else res
                else:
                    yield (category, m) if include_match else category

    return _search_all_regex


RUN_REGEXES_FUNC = search_all_regex_func(REGEXES)  # find all occurrences of all regexes
