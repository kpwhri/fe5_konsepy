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


def has_other_subject(text, direction=0, banned_characters='.'):
    """Return first mention of other subject

    direction = set to -1 (precontext) or 1 (postcontext) to ensure is in same sentence
    """
    if m := OTHER_SUBJECT_RX.search(text):
        if direction == -1:  # precontext
            for ch in banned_characters:
                if ch in text[m.end():]:
                    return None
        elif direction == 1:  # postcontext
            for ch in banned_characters:
                if ch in text[:m.start()]:
                    return None
        return m
    return None
