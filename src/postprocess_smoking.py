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


def postprocess_smoking(infile: Path, outfile: Path):
    logger.add(outfile.with_suffix('.log'))
    UNK = 'SmokingCategory.UNKNOWN'
    NO = 'SmokingCategory.NO'
    YES = 'SmokingCategory.YES'
    CURRENT = 'SmokingCategory.CURRENT'
    HISTORY = 'SmokingCategory.HISTORY'
    NEVER = 'SmokingCategory.NEVER'
    FAMILY = 'SmokingCategory.FAMILY'
    in_fieldnames = {UNK, YES, NO, CURRENT, HISTORY, NEVER, FAMILY}
    feature_labels = ['feature', 'fe_codetype', 'feature_status']
    features = {
        CURRENT: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'A'},
        NO: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'N'},
        HISTORY: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'H'},
        NEVER: {'feature': 'C0337672', 'fe_codetype': 'UC', 'feature_status': 'A'},
        YES: {'feature': 'C0337664', 'fe_codetype': 'UC', 'feature_status': 'A'},
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
                unk, yes, no, curr, hx, never, family = vals(row, UNK, YES, NO, CURRENT, HISTORY, NEVER, FAMILY)
                if (yes or curr) and not any([no, never]):  # only yes
                    write(YES)
                elif hx and not any([yes, curr, never]):
                    write(HISTORY)
                elif never and not any([yes, hx, curr]):
                    write(NEVER)
                elif no and not any([yes, hx, curr]):
                    write(NO)
                else:
                    if no > (curr + yes):
                        write(NO)
                    elif (curr + yes) > no:  # prefer yes if any admission
                        write(YES)
                    elif (hx + no) > yes:
                        write(HISTORY)
                    else:
                        pass  # unknown
                    if family:
                        pass  # family


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(fromfile_prefix_chars='!@')
    parser.add_argument('--infile', type=Path,
                        help='Input CSV file at appropriate level of analysis.')
    parser.add_argument('--outfile', type=Path,
                        help='Output CSV file with NLP features of FE Table.')
    args = parser.parse_args()

    postprocess_smoking(**vars(args))
