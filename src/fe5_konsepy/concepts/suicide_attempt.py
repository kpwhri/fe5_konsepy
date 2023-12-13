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
from fe5_konsepy.utils import get_precontext, get_postcontext, get_contexts


class SuicideAttempt(enum.Enum):  # TODO: change 'Concept' to relevant concept name
    """Start from 1; each must be distinct; use CAPITAL_LETTERS_WITH_UNDERSCORE is possible"""
    NO = 0
    YES = 1
    HISTORY = 2
    FAMILY = 3
    CODE = 4
    PROBLEM_LIST = 5  # YES, in problem list


suicide_attempt = '(?:{})'.format('|'.join([
    r'suicide\W+attempt',
    r'deliberate\W*self\W*harm',
    r'attempted\W*(?:to\W*commit\W*)?suicide',
    r'attempted\W*(?:\w+\W+){,2}to\W*take\W*(?:his|her)\W*(?:own\W*)?life',
    r'attempted\W*to\W*kill\W*(?:him|her)self',
]))

day = r'(?:\d{1,2}\W*)'
year = r'(?:\d{2,4})'
in_period = r'(?:in|on|during)\W*(?:{})'.format('|'.join([
    'college', 'university', 'childhood', r'(?:high|middle)\W*school', r'jr\W*high',
    rf'{day}?January\W*{year}?', rf'{day}?February\W*{year}?', rf'{day}?March\W*{year}?',
    rf'{day}?April\W*{year}?', rf'{day}?May\W*{year}?', rf'{day}?June\W*{year}?',
    rf'{day}?July\W*{year}?', rf'{day}?August\W*{year}?', rf'{day}?September\W*{year}?',
    rf'{day}?October\W*{year}?', rf'{day}?November\W*{year}?', rf'{day}?December\W*{year}?',
    r'(?:20|19)\d{2}', r'\d{1,2}/\d{1,4}(?:\d{2,4})?', 'the past',
]))

period_ago = r'(?:\d+|(?:a\W*)?few|one|two|three|a|several)\W*(?:month|week|year|day)s?\W*ago'

hx_of = r'(?:past|(?:history|hx)\W*of)'

deny = r'(?:den(?:y|ies|ied))'
family_hx = r'(?:family)'
no = r'(?:no)'


def check_if_other_subject(m, precontext, postcontext, **kwargs):
    if has_other_subject(precontext) or has_other_subject(postcontext):
        return SuicideAttempt.FAMILY
    return None


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
    (re.compile(rf'\b{deny}\W*{suicide_attempt}\W*{in_period}\b', re.I),
     SuicideAttempt.NO),
    (re.compile(rf'\b{deny}\W*{suicide_attempt}\W*{period_ago}\b', re.I),
     SuicideAttempt.NO),
    (re.compile(rf'\b{suicide_attempt}\W*{in_period}\b', re.I),
     SuicideAttempt.YES, [check_if_other_subject]),
    (re.compile(rf'\b{suicide_attempt}\W*{period_ago}\b', re.I),
     SuicideAttempt.YES, [check_if_other_subject]),
    (re.compile(rf'\b{hx_of}\W*{suicide_attempt}\s*:\s*(?:{deny}|{no})\b', re.I),
     SuicideAttempt.NO),
    (re.compile(rf'\b(?:{deny}|{no}|{family_hx})\W*{hx_of}\W*{suicide_attempt}\b', re.I),
     SuicideAttempt.NO),
    (re.compile(rf'\b{hx_of}\W*{suicide_attempt}\b', re.I),
     SuicideAttempt.YES, [check_if_other_subject, check_if_in_problem_list]),
    (re.compile(rf'\b(?:Z91.51|Z91.52|R45.88)\b'),
     SuicideAttempt.CODE),
]


def search_and_replace_regex_func(regexes, window=20):
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
