import sys
from pathlib import Path

from loguru import logger


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
            offset = max(0, context_match.start() - context_window)
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


def print_postprocessor_info(outdir: Path, concepts: list[str], file: Path | str, destdir: Path = None):
    """Print information for running the postprocessors on the command line.

    outdir: parameter specified when calling `run_all`
    concepts: the concepts specified
    destdir: may be None; the actual destination directory created
    """
    logger.info(f'To run the postprocessor and build the FE tables:')
    if len(concepts) != 1:
        logger.error(f'Postprocessor will probably run incorrectly:'
                     f' please specify one concept like `--concept smoking` or `--concept suicide_attempt`')
        if len(concepts) == 0:
            concepts = ['smoking']
    if not destdir:
        destdir = max(outdir.glob('run_all_*'), default=outdir / 'run_all_YYYYMMDD_HHMMSS')
        logger.warning(f'Guessed at the output directory so you may need to fix the `run_all` directory below'
                       f' to the correct run: {destdir}')
    concept = concepts[0]
    # get postproces_*.py filename
    file = Path(file)  # ensure not string
    if concept == 'smoking':
        target_file = file.parent / 'postprocess_smoking.py'
    elif concept == 'suicide_attempt':
        target_file = file.parent / 'postprocess_hx_attempted_suicide.py'
    else:
        logger.error(f'Unrecognized concept: {concept}')
        target_file = file.parent / 'postprocess_???????.py'
    cmd = (f'{sys.executable} {target_file}'
           f' --infile {destdir / "notes_category_counts.csv"}'
           f' --outdir {destdir / concept}')
    logger.info(f'>> {cmd}')
