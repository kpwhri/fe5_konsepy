import enum
import re

from konsepy.regex import search_all_regex


class SmokingCategory(enum.Enum):
    """Start from 1; each must be distinct; use CAPITAL_LETTERS_WITH_UNDERSCORE is possible"""
    NO = 0
    CURRENT = 1
    HISTORY = 2
    NEVER = 3
    YES = 4


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
smoke_target = r'(?:marijuana|cigarettes?|cigars?)'
curr_smokes = r'(?:smokes)'
past_smoked = r'(?:smoked|used to smoke)'


def check_if_zero(m):
    val = float(m.group('num'))
    if val:
        return SmokingCategory.HISTORY
    return None


REGEXES = [
    (re.compile(rf'\b{smoking_history}\b', re.I), SmokingCategory.HISTORY),
    (re.compile(rf'\b{former}\W*{smoker}\b', re.I), SmokingCategory.HISTORY),
    (re.compile(rf'\b{no_longer}\W*{smoking}\b', re.I), SmokingCategory.HISTORY),
    (re.compile(rf'\bnever\W*{smoking}\b', re.I), SmokingCategory.NEVER),
    (re.compile(rf'\b{current}\W*{smoker}\b', re.I), SmokingCategory.CURRENT),
    (re.compile(rf'\b{packs_per_day}\W*(?P<num>{digit})\b', re.I), SmokingCategory.NO, check_if_zero),
    (re.compile(rf'\b{pack_years}\W*(?P<num>{digit})\b', re.I), SmokingCategory.NEVER, check_if_zero),
    (re.compile(rf'\b(?P<num>{digit})\W*{packs_per_day}\b', re.I), SmokingCategory.NO, check_if_zero),
    (re.compile(rf'\b(?P<num>{digit})\W*{pack_years}\b', re.I), SmokingCategory.NEVER, check_if_zero),
    (re.compile(rf'\b{smoking_status}\W*{never}\b', re.I), SmokingCategory.NEVER),
    (re.compile(rf'\b{smoking_status}\W*(?:{former})\b', re.I), SmokingCategory.HISTORY),
    (re.compile(rf'\b{smoking_status}\W*(?:{current})\b', re.I), SmokingCategory.CURRENT),
    (re.compile(rf'\b{curr_smokes}\W*{smoke_target}\b', re.I), SmokingCategory.CURRENT),
    (re.compile(rf'\b{past_smoked}\W*{smoke_target}\b', re.I), SmokingCategory.HISTORY),
]


def search_all_regex_func(regexes):
    """For each regex, return all, but run 3rd argument if a function (use finditer)"""

    def _search_all_regex(text):
        for regex, category, *other in regexes:
            func = None
            if len(other) > 0:
                func = other[0]
            for m in regex.finditer(text):
                if func and (res := func(m)):
                    yield res
                else:
                    yield category

    return _search_all_regex


RUN_REGEXES_FUNC = search_all_regex_func(REGEXES)  # find all occurrences of all regexes
