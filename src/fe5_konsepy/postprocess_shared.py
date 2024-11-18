import csv
from abc import abstractmethod
from pathlib import Path

from loguru import logger

from fe5_konsepy import __version__

import datetime


class Postprocessor:

    def __init__(self, name, pipeline_id=None, description='Regular expression-based pipeline in konsepy.'):
        self.now_dt = datetime.datetime.now()
        self.now_str = self.now_dt.strftime('%Y%m%d_%H%M%S')
        self.run_name = f'{name}_{self.now_str}'
        self.pipeline_id = pipeline_id or int(str(hash(self.run_name))[-8:])
        self.description = description
        self.feature_labels = ['feature', 'fe_codetype', 'feature_status', 'pipeline_id']
        self.load_categories()
        self.features = {x: y | {'pipeline_id': self.pipeline_id} for x, y in self.get_features().items()}

    @abstractmethod
    def load_categories(self):
        pass

    @abstractmethod
    def get_features(self):
        pass

    @abstractmethod
    def process_row(self):
        pass

    def postprocess(self, infile: Path, outdir: Path):
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

    def val(self, data, col):
        d = data[col]
        if d:
            return int(d)
        return 0

    def vals(self, data, *cols):
        return [self.val(data, col) for col in cols]

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
