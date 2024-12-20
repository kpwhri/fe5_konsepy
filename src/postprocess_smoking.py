from pathlib import Path

from fe5_konsepy.postprocess_shared import Postprocessor, run_postprocessing


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
        self.UNK_NEVER = 'UNKNOWN_NEVER'
        self.NOT_NEVER = 'NOT_NEVER'

    def get_features(self):
        return {
            self.CURRENT: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'A'},
            self.NO: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'N'},
            self.HISTORY: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'H'},
            self.NEVER: {'feature': 'C0337672', 'fe_codetype': 'UC', 'feature_status': 'A'},
            self.YES: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'A'},
            self.UNK_NEVER: {'feature': 'C0337672', 'fe_codetype': 'UC', 'feature_status': 'U'},
            self.NOT_NEVER: {'feature': 'C0337672', 'fe_codetype': 'UC', 'feature_status': 'N'},
            self.UNK: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'A'},
        }

    def process_row(self, row, write):
        unk, yes, no, curr, hx, never, family = self.vals(
            row, self.UNK, self.YES, self.NO, self.CURRENT, self.HISTORY, self.NEVER, self.FAMILY
        )
        if (yes or curr) and not any([no, never]):  # only yes
            write(self.YES)
            write(self.NOT_NEVER)
        elif hx and not any([yes, curr, never]):
            write(self.HISTORY)
            write(self.NOT_NEVER)
        elif never and not any([yes, hx, curr]):
            write(self.NEVER)
            write(self.NO)
        elif no and not any([yes, hx, curr]):
            write(self.NO)
            write(self.UNK_NEVER)
        else:
            if no > (curr + yes):
                write(self.NO)
                write(self.UNK_NEVER)
            elif (curr + yes) > no:  # prefer yes if any admission
                write(self.YES)
                write(self.NOT_NEVER)
            elif (hx + no) > yes:
                write(self.HISTORY)
                write(self.NOT_NEVER)
            else:
                write(self.UNK)  # unknown
                write(self.UNK_NEVER)  # unknown
            if family:
                pass  # family history -- not relevant in this context


def postprocess_smoking(infile: Path, outdir: Path = None, pipeline_id=None, remove_ctrl=False):
    pp = SmokingPostprocessor(
        'fe5_konsepy-smoking',
        pipeline_id,
        'Regular expression-based pipeline to extract smoking status.',
        remove_ctrl,
    )
    pp.postprocess(infile, outdir)


if __name__ == '__main__':
    run_postprocessing(postprocess_smoking)
