import re

OTHER_SUBJECT_RX = re.compile('(?:{})'.format(
    '|'.join(rf'\b{x}\'?\b' for x in [
        'brother', 'sister', 'sibling', 'mother', 'mom', 'father', 'dad',
        'parent', 'dtr', 'daughter', 'son', 'child', 'children',
        'aunt', 'uncle', 'niece', 'nephew', 'cousin',
        'gma', 'grandma', 'grandmother', 'gpa', 'grandpa', 'grandfather', 'grandparent',
        r'grand\W?daughter', 'gdtr',
        'husb(?:and)?', 'wife', 'wives', 'spouse', 'partner', r'girl\W?friendboy\W?friend',
        'neighbou?r', r'significant\W*other', 'person',
        'people', 'friend', 'kid', 'peer',
        'physician', 'doctor', 'family', r'co\W?worker',
        r'(?:house|room|flat)\W?mate', 'colleague', 'employe[re]', 'others',
        'family (?:history|hx)',
    ]))
)


def has_other_subject(text):
    """Return first mention of other subject"""
    if m := OTHER_SUBJECT_RX.search(text):
        return m
    return None
