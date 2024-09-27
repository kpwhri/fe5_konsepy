import csv
from loguru import logger
from pathlib import Path


def val(data, col):
    d = data[col]
    if d:
        return int(d)
    return 0


def vals(data, *cols):
    return [val(data, col) for col in cols]


def postprocess_hx_attempted_suicide(infile: Path, outfile: Path):
    logger.add(outfile.with_suffix('.log'))
    NO = 'SuicideAttempt.NO'
    YES = 'SuicideAttempt.YES'
    HISTORY = 'SuicideAttempt.HISTORY'
    FAMILY = 'SuicideAttempt.FAMILY'
    CODE = 'SuicideAttempt.CODE'
    PROBLEM_LIST = 'SuicideAttempt.PROBLEM_LIST'
    in_fieldnames = {YES, NO, HISTORY, FAMILY, CODE, PROBLEM_LIST}
    feature_labels = ['feature', 'fe_codetype', 'feature_status']
    features = {
        YES: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'A'},
        NO: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'N'},
        FAMILY: {'feature': 'C0455507', 'fe_codetype': 'UC', 'feature_status': 'X'},
    }

    def write(feature):
        writer.writerow({col: row[col] for col in included_names} | features[feature])

    with open(outfile, 'w', encoding='utf-8', newline='') as out:
        with open(infile, encoding='utf8') as fh:
            reader = csv.DictReader(fh)
            included_names = list(set(reader.fieldnames) - in_fieldnames)
            writer = csv.DictWriter(out, fieldnames=included_names + feature_labels)
            writer.writeheader()
            for row in reader:
                code, pl, yes, no, family, hx = vals(row, CODE, PROBLEM_LIST, YES, NO, FAMILY, HISTORY)
                if code or pl:
                    write(YES)
                elif (yes or hx) and not any([no, family]):  # only yes
                    write(YES)
                elif no and not any([yes, family, hx]):
                    write(NO)
                elif family and not any([yes, no, hx]):
                    write(FAMILY)
                else:
                    if (yes + hx) > (family + no + 1):  # yes must be much more common
                        write(YES)
                    if family:
                        write(FAMILY)
                    if no >= (yes + hx):
                        write(NO)
                # certain cases, e.g., `yes-1 = no, where no > 0` determined to be 'too close to call'


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='!@')
    parser.add_argument('--infile', type=Path,
                        help='Input CSV file at appropriate level of analysis.')
    parser.add_argument('--outfile', type=Path,
                        help='Output CSV file with NLP features of FE Table.')
    args = parser.parse_args()

    postprocess_hx_attempted_suicide(**vars(args))
