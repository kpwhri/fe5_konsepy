

def get_precontext(m, text, window=20):
    """
    TODO: add word window
    """
    return text[max(0, m.start() - window): m.start()]


def get_postcontext(m, text, window=20):
    return text[m.end(): m.end() + window]


def get_contexts(m, text, window=20):
    return {
        'precontext': get_precontext(m, text, window),
        'postcontext': get_postcontext(m, text, window),
        'text': text,
    }