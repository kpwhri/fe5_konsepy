import pytest

# TODO: change `example_nlp` to $PROJECT_NAME
# TODO: update `new_concept_template` to filename
# TODO: update `ConceptCategory` to correct concept label
from example_nlp.concepts.new_concept_template import ConceptCategory, REGEXES
from konsepy.regex import search_first_regex


@pytest.mark.parametrize('text, exp', [
    ('Text excerpt containing concept.', ConceptCategory.YES),  # TODO: put tests here
    # add more tests
])
def test_run_regexes(text, exp):
    results = set(search_first_regex(REGEXES)(text))
    assert exp in results
