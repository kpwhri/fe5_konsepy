from pathlib import Path

from fe5_konsepy.postprocess_shared import Postprocessor, run_postprocessing


class HxSAPostprocessor(Postprocessor):

    def get_features(self):
        return {
            self.YES: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'A'},
            self.NO: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'N'},
            self.FAMILY: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'X'},
        }

    def process_row(self, row, write):
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
        # certain cases, e.g., `yes-1 = no, where no > 0` determined to be 'too close to call'

    def load_categories(self):
        self.NO = 'SuicideAttempt.NO'
        self.YES = 'SuicideAttempt.YES'
        self.HISTORY = 'SuicideAttempt.HISTORY'
        self.FAMILY = 'SuicideAttempt.FAMILY'
        self.CODE = 'SuicideAttempt.CODE'
        self.PROBLEM_LIST = 'SuicideAttempt.PROBLEM_LIST'
        self.in_fieldnames = {self.YES, self.NO, self.HISTORY, self.FAMILY, self.CODE, self.PROBLEM_LIST}


def postprocess_hx_attempted_suicide(infile: Path, outdir: Path = None, pipeline_id=None, remove_ctrl=False):
    pp = HxSAPostprocessor(
        'fe5_konsepy-hx_suicide_attempt',
        pipeline_id,
        'Regular expression-based pipeline to extract history of self-harm and suicide attempts.',
        remove_ctrl,
    )
    pp.postprocess(infile, outdir)


if __name__ == '__main__':
    run_postprocessing(postprocess_hx_attempted_suicide)
