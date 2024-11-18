from pathlib import Path

from fe5_konsepy.postprocess_shared import Postprocessor


class SmokingPostprocessor(Postprocessor):

    def load_categories(self):
        self.UNK = 'SmokingCategory.UNKNOWN'
        self.NO = 'SmokingCategory.NO'
        self.YES = 'SmokingCategory.YES'
        self.CURRENT = 'SmokingCategory.CURRENT'
        self.HISTORY = 'SmokingCategory.HISTORY'
        self.NEVER = 'SmokingCategory.NEVER'
        self.FAMILY = 'SmokingCategory.FAMILY'
        self.in_fieldnames = {self.UNK, self.YES, self.NO, self.CURRENT, self.HISTORY, self.NEVER, self.FAMILY}

    def get_features(self):
        return {
            self.CURRENT: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'A'},
            self.NO: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'N'},
            self.HISTORY: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'H'},
            self.NEVER: {'feature': 'C0337672', 'fe_codetype': 'UC', 'feature_status': 'A'},
            self.YES: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'A'},
        }

    def process_row(self, row, write):
        unk, yes, no, curr, hx, never, family = self.vals(
            row, self.UNK, self.YES, self.NO, self.CURRENT, self.HISTORY, self.NEVER, self.FAMILY
        )
        if (yes or curr) and not any([no, never]):  # only yes
            write(self.YES)
        elif hx and not any([yes, curr, never]):
            write(self.HISTORY)
        elif never and not any([yes, hx, curr]):
            write(self.NEVER)
        elif no and not any([yes, hx, curr]):
            write(self.NO)
        else:
            if no > (curr + yes):
                write(self.NO)
            elif (curr + yes) > no:  # prefer yes if any admission
                write(self.YES)
            elif (hx + no) > yes:
                write(self.HISTORY)
            else:
                pass  # unknown
            if family:
                pass  # family


def postprocess_smoking(infile: Path, outdir: Path, pipeline_id=None):
    pp = SmokingPostprocessor(
        'fe5_konsepy-smoking',
        pipeline_id,
        'Regular expression-based pipeline to extract smoking status.',
    )
    pp.postprocess(infile, outdir)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='!@')
    parser.add_argument('--infile', type=Path,
                        help='Input CSV file at appropriate level of analysis '
                             '(notes_category_counts.csv for note-level).')
    parser.add_argument('--outdir', type=Path,
                        help='Output directory to place table definitions as CSV files.')
    parser.add_argument('--pipeline-id', dest='pipeline_id', type=int, default=None,
                        help='Specify the Pipeline ID (aka Feature ID) to be included with this run.')
    args = parser.parse_args()

    postprocess_smoking(**vars(args))