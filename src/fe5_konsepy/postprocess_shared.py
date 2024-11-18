import csv
import json
from abc import abstractmethod
from pathlib import Path

from loguru import logger
import unicodedata

from fe5_konsepy import __version__

import datetime


class Postprocessor:

    def __init__(self, name, pipeline_id=None,
                 description='Regular expression-based pipeline in konsepy.',
                 remove_ctrl=False):
        self.now_dt = datetime.datetime.now()
        self.now_str = self.now_dt.strftime('%Y%m%d_%H%M%S')
        self.remove_ctrl = remove_ctrl
        self.run_name = f'{name}_{self.now_str}'
        self.pipeline_id = pipeline_id or int(str(hash(self.run_name))[-8:])
        self.description = description
        self.feature_labels = ['feature', 'fe_codetype', 'feature_status', 'pipeline_id', 'confidence']
        self.load_categories()
        feature_plus = {'pipeline_id': self.pipeline_id, 'confidence': 'N'}
        self.features = {x: y | feature_plus for x, y in self.get_features().items()}
        self.default_feature_set = {'feature': None, 'fe_codetype': None, 'feature_status': None} | feature_plus

    @abstractmethod
    def load_categories(self) -> None:
        """This function should add attributes to the class, and `self.in_fieldnames` being a set of all of them

        E.g.,
        self.NO = 'SuicideAttempt.NO'
        self.YES = 'SuicideAttempt.YES'
        self.HISTORY = 'SuicideAttempt.HISTORY'
        self.FAMILY = 'SuicideAttempt.FAMILY'
        self.CODE = 'SuicideAttempt.CODE'
        self.PROBLEM_LIST = 'SuicideAttempt.PROBLEM_LIST'
        self.in_fieldnames = {self.YES, self.NO, self.HISTORY, self.FAMILY, self.CODE, self.PROBLEM_LIST}
        """
        pass

    @abstractmethod
    def get_features(self) -> dict[str, dict]:
        """This function should return a dict of features

        E.g.,
        return {
            self.YES: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'A'},
            self.NO: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'N'},
            self.FAMILY: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'X'},
        }
        """
        pass

    @abstractmethod
    def process_row(self, row, write):
        """This function should include logic for parsing a row of data and determining how to summarize the info.

        E.g.,
        code, pl, yes, no, family, hx = self.vals(
            row, self.CODE, self.PROBLEM_LIST, self.YES, self.NO, self.FAMILY, self.HISTORY
        )
        if code or pl:
            write(self.YES)
        elif (yes or hx) and not any([no, family]):  # only yes
            write(self.YES)
        elif no and not any([yes, family, hx]):
            write(self.NO)
        elif family and not any([yes, no, hx]):
            write(self.FAMILY)
        else:
            if (yes + hx) > (family + no + 1):  # yes must be much more common
                write(self.YES)
            if family:
                write(self.FAMILY)
            if no >= (yes + hx):
                write(self.NO)
        """
        pass

    def postprocess(self, infile: Path, outdir: Path):
        outdir.mkdir(exist_ok=True)
        logger.add(outdir / f'{self.run_name}.log')
        fe_table = outdir / 'fe_feature_table.csv'
        pipeline_table = outdir / 'fe_pipeline_table.csv'
        detail_table = outdir / 'fe_feature_detail_table.csv'

        self.write_pipeline_version_info(pipeline_table)

        def write(feature):
            writer.writerow({col: row[col] for col in included_names} | self.features[feature])

        with open(fe_table, 'w', encoding='utf8', newline='') as out:
            with open(infile, encoding='utf8') as fh:
                reader = csv.DictReader(fh)
                included_names = list(set(reader.fieldnames) - self.in_fieldnames)
                writer = csv.DictWriter(out, fieldnames=included_names + self.feature_labels)
                writer.writeheader()
                for row in reader:
                    self.process_row(row, write)

        output_jsonl = infile.parent / 'output.jsonl'
        if not output_jsonl.exists():
            logger.warning(f'Cannot create FE_FEATURE_DETAIL table: cannot find `output_jsonl` at {output_jsonl}.')
        else:
            logger.info(f'Generating FE_FEATURE_DETAIL table using: {output_jsonl}')
            details_fieldnames = ['studyid', 'note_id', 'note_date', 'start_index', 'end_index', 'matched_text',
                                  ] + self.feature_labels
            with open(detail_table, 'w', encoding='utf8', newline='') as out:
                writer = csv.DictWriter(out, fieldnames=details_fieldnames)
                writer.writeheader()
                with open(output_jsonl, encoding='utf8') as fh:
                    for line in fh:
                        data = json.loads(line.strip())
                        for category, (matched_text, start_idx, end_idx) in zip(data['categories'], data['matches']):
                            writer.writerow(
                                {
                                    'studyid': data['studyid'],
                                    'note_id': data['note_id'],
                                    'note_date': data['note_date'],
                                    'start_index': start_idx,
                                    'end_index': end_idx,
                                    'matched_text': self.clean(matched_text),
                                } | self.features.get(category, self.default_feature_set)
                            )

    def val(self, data, col):
        d = data[col]
        if d:
            return int(d)
        return 0

    def vals(self, data, *cols):
        return [self.val(data, col) for col in cols]

    def clean(self, text):
        text = ' '.join(text.split())
        if self.remove_ctrl:
            return ''.join(c if unicodedata.category(c)[0] != 'C' else '?' for c in text)
        return text

    def write_pipeline_version_info(self, outfile):
        fieldnames = ['id', 'name', 'version', 'run_date', 'description', 'source']
        with open(outfile, 'w', encoding='utf8', newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'id': self.pipeline_id,
                'name': self.run_name,
                'version': __version__,
                'run_date': self.now_dt.strftime('%Y-%m-%d'),
                'description': self.description,
                'source': 'https://github.com/kpwhri/fe5_konsepy'
            })


def run_postprocessing(func):
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='!@')
    parser.add_argument('--infile', type=Path,
                        help='Input CSV file at appropriate level of analysis '
                             '(notes_category_counts.csv for note-level).')
    parser.add_argument('--outdir', type=Path,
                        help='Output directory to place table definitions as CSV files.')
    parser.add_argument('--pipeline-id', dest='pipeline_id', type=int, default=None,
                        help='Specify the Pipeline ID (aka Feature ID) to be included with this run.')
    parser.add_argument('--remove-ctrl', dest='remove_ctrl', action='store_true', default=False,
                        help='Include thsi flag to replace all control characters with "?" in the matched text.')
    return func(**vars(parser.parse_args()))
