"""
This file should not be edited. It is just a template for creating additional templates.

Steps for creating a new category:
1. Copy-paste this file to $PROJECT_PATH/src/$PROJECT_NAME/concepts
2. Name new file something like `concept.py`
3. Fix statements on the relevant lines marked # TODO
4. Copy-paste `test_concept_template` file in tests directory
5. Name new file to something like `test_concept.py`
6. Fix statements on relevant lines marked # TODO
7. Add `ConceptCategory` and `RUN_REGEXES_FUNC` to `run_all.py`
8. (Less important) Add the `run_file_on_concept` function to the `tests/test_run_regex_and_output` file.
"""
import enum
import re

from fe5_konsepy.other_subject import has_other_subject
from fe5_konsepy.utils import get_contexts


class SuicideAttempt(enum.Enum):  # TODO: change 'Concept' to relevant concept name
    """Start from 1; each must be distinct; use CAPITAL_LETTERS_WITH_UNDERSCORE is possible"""
    NO = 0
    YES = 1
    HISTORY = 2
    FAMILY = 3
    CODE = 4
    PROBLEM_LIST = 5  # YES, in problem list


suicide_attempt = '(?:{})'.format('|'.join([
    r'suicide\W+attempts?',
    r'deliberate\W*self\W*harm',
    r'self\W*harm\W*behaviou?r',
    r'attempted\W*(?:to\W*commit\W*)?suicide',
    r'attempted\W*(?:\w+\W+){,2}to\W*take\W*(?:his|her)\W*(?:own\W*)?life',
    r'attempted\W*to\W*kill\W*(?:him|her)self',
]))

day = r'(?:\d{1,2}\W*)'
year = r'(?:\d{2,4})'
in_period = r'(?:in|on|during)\W*(?:\w+\W+)?(?:{})'.format('|'.join([
    'college', 'university', 'childhood', r'(?:high|middle)\W*school', r'jr\W*high',
    'teens', 'twenties', 'thirties', r'\d0s',
    rf'{day}?January\W*{year}?', rf'{day}?February\W*{year}?', rf'{day}?March\W*{year}?',
    rf'{day}?April\W*{year}?', rf'{day}?May\W*{year}?', rf'{day}?June\W*{year}?',
    rf'{day}?July\W*{year}?', rf'{day}?August\W*{year}?', rf'{day}?September\W*{year}?',
    rf'{day}?October\W*{year}?', rf'{day}?November\W*{year}?', rf'{day}?December\W*{year}?',
    r'(?:20|19)\d{2}', r'\d{1,2}/\d{1,4}(?:\d{2,4})?', 'the past',
]))

approximately = rf'(?:about|approximately|almost|close\W*to|nearly|just\W*about)'
more_than = fr'(?:(?:over|(?:more|less)\s*than|{approximately})\W*)?'
period_ago = rf'{more_than}(?:\d+|(?:a\W*)?few|one|two|three|a|several)\W*(?:month|week|year|day)s?\W*ago'
as_a = r'(?:as a|when a)'
role_label = r'(?:teen(?:ager)?|freshman|jr|junior|senior|sr|sophomore|student)'
role_descript = r'(?:college|(?:high|middle) school)'
role = rf'{role_label}\W*(?:in|at|during)\W*{role_descript}'
role_rev = fr'(?:{role_descript}\W*)?{role_label}'
as_a_role = rf'(?:{as_a}\W*(?:{role}|{role_rev}))'

hx_of = r'(?:past|(?:history|hx)\W*of|previous|prior)'

deny = r'(?:den(?:y|ies|ied))'
family_hx = r'(?:family)'
no = r'(?:no|or|nor|not)'
yes = r'(?:yes|briefly|previously)'
number = r'(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen)'
times = rf'(?:{number}\s*(?:x|times?))'
more_than_times = rf'{more_than}{times}'
age = rf'(?:at\W*)?age\W*{number}'
sa_predicate = rf'(?:{approximately}\W*)?(?:{in_period}|{period_ago}|{more_than_times}|{as_a_role}|{age})'

# per/according to/at X's house
PER_PAT = re.compile(r'(?:\bper\b|according\W*to|\bat\b|\bdue\W*to\b|because\W*of\b)(?:\W+\w+)?\W*$', re.I)
OBJECT_PAT = re.compile(r'(?:\w+\W+)?(?:med\w*|gun|weapon|pill)s?', re.I)


def is_not_other_subject(m, precontext, postcontext, **kwargs):
    """Exceptions to other subject pattern"""
    if PER_PAT.search(precontext) or OBJECT_PAT.search(postcontext):
        return True


def check_if_other_subject(m, precontext, postcontext, text, window, **kwargs):
    if m2 := has_other_subject(precontext, direction=-1):
        direction = -1
    elif m2 := has_other_subject(postcontext, direction=1):
        direction = 1
    if m2:
        if is_not_other_subject(m2, **get_contexts(
                m2, text, context_match=m, context_window=window, context_direction=direction
        )):
            return None
        return SuicideAttempt.FAMILY
    return None


def check_if_colon_before(m, precontext, **kwargs):
    if precontext.strip().endswith(':'):
        return True


def check_if_in_problem_list(m, text, **kwargs):
    prev_match = None
    for problist_match in re.finditer(r'(?:(?:PMH|Medical History):|problem list:?)', text, re.I):
        if problist_match.start() > m.end():  # occurs after current match
            break
        prev_match = problist_match
    if prev_match:
        target_text = text[prev_match.end():m.start()].lower()
        for skipper in [':', 'medications']:
            if skipper in target_text:  # found section in between
                return None
        return SuicideAttempt.PROBLEM_LIST
    else:
        return None


REGEXES = [
    (re.compile(rf'\b{deny}\W*{suicide_attempt}\W*{sa_predicate}\b', re.I),
     SuicideAttempt.NO),
    # must be above SA SA_pred due to 'denies hx of SA in teens'
    (re.compile(rf'\b(?:{deny}|{no})\W*(?:\w+\W*)?{hx_of}\W*{suicide_attempt}\b', re.I),
     SuicideAttempt.NO, [check_if_colon_before]),
    (re.compile(rf'\b(?:{family_hx})\W*(?:\w+\W*)?{hx_of}\W*{suicide_attempt}\b', re.I),
     SuicideAttempt.FAMILY, [check_if_colon_before]),
    (re.compile(rf'\b{suicide_attempt}\W*{sa_predicate}\b', re.I),
     SuicideAttempt.YES, [check_if_other_subject]),
    (re.compile(rf'\b{hx_of}\W*{suicide_attempt}\s*:\s*(?:{deny}|{no})\b', re.I),
     SuicideAttempt.NO),
    # specific (optional <- these get caught by next regex; can't move up otherwise 'denied hx of sa in teens')
    (re.compile(
        rf'\b{hx_of}\W*{suicide_attempt}\s*:\s*(?:{yes}|{number}|{sa_predicate})\b', re.I),
     SuicideAttempt.YES),
    # more generic
    (re.compile(rf'\b{hx_of}\W*{suicide_attempt}\b', re.I),
     SuicideAttempt.YES, [check_if_other_subject, check_if_in_problem_list]),
    (re.compile(rf'\b(?:Z91.51|Z91.52|R45.88)\b'),
     SuicideAttempt.CODE),
]


def search_and_replace_regex_func(regexes, window=30):
    """Search, but replace found text to prevent double-matching"""

    def _search_all_regex(text, include_match=False):
        for regex, category, *other in regexes:
            funcs = None
            if len(other) > 0:
                funcs = other[0]
            text_pieces = []
            prev_end = 0
            for m in regex.finditer(text):
                found = None
                if funcs:
                    for func in funcs:  # parse function in order
                        if res := func(m, **get_contexts(m, text, window)):
                            found = (res, m) if include_match else res
                            break
                if found:
                    if found is True or (include_match and found[0] is True):
                        continue  # no result
                    yield found
                else:
                    yield (category, m) if include_match else category
                text_pieces.append(text[prev_end:m.start()])
                text_pieces.append(f" {(len(m.group()) - 2) * '.'} ")
                prev_end = m.end()
            text_pieces.append(text[prev_end:])
            text = ''.join(text_pieces)

    return _search_all_regex


RUN_REGEXES_FUNC = search_and_replace_regex_func(REGEXES)  # find all occurrences of all regexes
