def get_precontext(m, text, window=20, start=None):
    """
    TODO: add word window
    """
    if start is None:
        start = m.start()
    return text[max(0, start - window): start]


def get_postcontext(m, text, window=20, end=None):
    if end is None:
        end = m.end()
    return text[end: end + window]


def get_contexts(m, text, window=20, context_match=None, context_window=None, context_direction=0):
    """
    if matching on context of a previous match, the offsets will need to be updated. To do this, use:
        * context_match: previous match
        * context_window: previous window (supplied by `window` parameter)
        * context_direction: -1 for previous context, 1 for post-context
    """
    if context_match:
        if context_direction == -1:
            offset = context_match.start() - context_window
            start = offset + m.start()
            end = offset + m.end()
        elif context_direction == 1:
            offset = context_match.end()
            start = offset + m.start()
            end = offset + m.end()
        else:
            raise ValueError(fr'Unrecognized context direction: {context_direction};'
                             ' expected -1 [before] or +1 [after]')
        precontext = get_precontext(m, text, window, start=start)
        postcontext = get_postcontext(m, text, window, end=end)
    else:
        precontext = get_precontext(m, text, window)
        postcontext = get_postcontext(m, text, window)
    return {
        'precontext': precontext,
        'postcontext': postcontext,
        'text': text,
        'window': window,
    }
