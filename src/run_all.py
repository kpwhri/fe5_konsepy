"""
Run all concepts and place multiple files into an output directory.

Usage:
    python run_all.py --input-files data.csv --outdir out --id-label studyid
"""
from pathlib import Path

from konsepy.cli import add_outdir_and_infiles, add_run_all_args
from konsepy.run_all import run_all
from loguru import logger

from config import PACKAGE_NAME
from fe5_konsepy.utils import print_postprocessor_info


def run_all_concepts(input_files, outdir: Path,
                     id_label, noteid_label, notedate_label, notetext_label, noteorder_label=None,
                     incremental_output_only=False, concepts=None, **kwargs):
    if not concepts:
        logger.warning(f'You probably want to specify a concept if using this for FE5 work;'
                       f' e.g., `--concept smoking` or `--concept suicide_attempt`')
        concepts = []
    elif len(concepts) > 1:
        logger.warning(f'For FE5 work, it is preferred to specify only a single concept;'
                       f' e.g., `--concept smoking` or `--concept suicide_attempt` rather than {concepts}')
    destdir = run_all(
        input_files, outdir, PACKAGE_NAME,
        id_label=id_label, noteid_label=noteid_label,
        notedate_label=notedate_label, notetext_label=notetext_label,
        noteorder_label=noteorder_label, incremental_output_only=incremental_output_only,
        concepts=concepts, **kwargs
    )
    print_postprocessor_info(outdir, concepts, __file__, destdir)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@!')
    add_outdir_and_infiles(parser)
    add_run_all_args(parser)
    run_all_concepts(**vars(parser.parse_args()))
