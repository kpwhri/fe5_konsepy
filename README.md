# FE5 Variables with Konsepy NLP

Implementation of FE5 variables using the konsepy NLP framework.

## About/Terminology

Konsepy works around the idea of a `concept`. A `concept` is a semantic category which might have multple
representations in text. For example, a concept might be SOCIAL_ISOLATION which targets any text describing this in
text (e.g., 'no friends', 'lacks social support', etc.). Another could be COUGHING which might be described in text as '
coughs', 'hacking', 'wheeze', etc. The selection of concepts will depend on the particular application. If you only care
about a single output category, it's sufficient to just have a single target concept.

Each `concept` is assigned a set of regular expressions which are used to assign a concept to a section of text. These
regular expressions each receive an individual label.

## Getting Started

### Prerequisites

* Python 3.9+
* Download/clone this project
    * The path to this location will be referred to as `$PATH` in the instructions below (this might be `C:\code`, etc.)
* (Optional, but recommended) setup a virtual environment to isolate this particular installation
    * `cd $PATH\fe5_konsepy`
    * `python -m venv .venv`
        * The full path to `python.exe` might need to be specified in this command
    * Activate:
        * Powershell: `.venv/scripts/activate.ps1`
        * Linux/Mac: `source .venv/bin/activate`
* Install required packages:
    * `pip install requirements.txt`
    * OR `pip install .`
* A corpus file
    * In the future, other data sources will be included, for now it must be `csv`, `jsonl`, `sas7bdat`
    * Columns (these can be configured to use different names, but it's easiest if you select these names)
        * `studyid`: (required) subject-level identifier; if not important/relevant, set all instances to `1`
        * `note_id`: (required) note-level identifier; unique identifier for each note
        * `note_text`: (required) text associated with each note
        * `note_date`: (optional) date of note; not used by algorithm so probably easiest to ignore
        * `note_line`: (optional) if note broken into multiple segments (see example in `sample/corpus_lined.csv`),
          specify this to join them
            * If using `note_line`, all portions of the note are assumed to appear together in the dataset (i.e., order
              by `note_id, note_line`)
        * corpus may contain other columns which will be ignored

### Running

* To run the pipeline on a CSV file:
    * `python src/run_all.py --input-files sample/corpus.csv --outdir out --id-label studyid`
* To run just the `smoking` pipeline on a CSV file:
    * `python src/run_concept.py --input-files sample/corpus.csv --outdir out --id-label studyid --concept smoking`
* To run just the `suicide_attempt` pipeline on a CSV file:
    *
  `python src/run_concept.py --input-files sample/corpus.csv --outdir out --id-label studyid --concept suicide_attempt`

If you need to specify different headers/variables/labels to your corpus file, use the following command line
arguments (the defaults are shown):

* `--id-label studyid`
* `--noteid-label note_id`
* `--notedate-label note_date`
* `--notetext-label note_text`

### Postprocessing

Once the target concepts have been identified, they will be output to CSV files in a the output directory starting with
the labels `run_all_{YYYYMMDD_HHMMSS}`. Within this folder

* For patient-level information, consider `mrn_category_counts.csv`
* For note-level information, consider `notes_category_counts.csv`

The postprocessing step attempts to summarize the disparate counts/values extracted into a single concluding value to be
populated to the FE Table. In certain cases, a single note might produce multiple output values (i.e., 1 note will
equate to multiple lines in the FE table).

#### Any Changes to Category Counts?

While it is recommended to run postprocessing at the note-level (`notes_catgory_counts.csv`), you can perform
summarization at a different level of analysis. E.g., to analyze by day/encounter, we might need to first group multiple
notes together. The steps might be:

1. Merge `notes_category_counts.csv` with a table that maps `note_id` to `encounter_id`
2. Group by `mrn` (or `studyid`) and `encounter_id` and aggregate the counts with `sum`.
    * NB: `0` is left empty rather than output, so you may need to transform these missing values to `0` first
3. Run the postprocessing

#### Running Postprocessing

There are two different files for running post-processing, depending on whether the target is smoking status or history
of suicide attempt. They accept the same arguments. These will create a new file with all of the same metadata, but
replace the extracted concepts with the following headers/variables/columns:

* **feature**: the corresponding CUI to the concept
* **fe_codetype**: `UC` (for UMLS CUI)
* **feature_status**: any contextual conditions on the future (e.g., negated)
    * `A`: affirmed
    * `X`: other subject
    * `H`: historical
    * `N`: negated

**smoking**

```commandline
python src/postprocess_smoking.py --infile notes_category_counts.csv --outfile fe_table_smoking.csv
```

**suicide_attempt**

```commandline
python src/postprocess_hx_attempted_suicide.py --infile notes_category_counts.csv --outfile fe_table_hxsa.csv
```

### Storing Version Information

It is probably important to store the version information in a separate table, linking with a unique `PipelineID` (or
`FeatureID` as currently defined).

* **Pipeline name**: fe5_konsepy
* **Source**: https://github.com/kpwhri/fe5_konsepy
* **Version**: 0.0.3
    * You can get this information by either:
        * Looking in `src/fe5_konsepy/__init__.py`
        * Looking at the most recent version at the top of `CHANGELOG.md`
        * Running `git tag -l` and selecting the largest (likely bottom) version number

## Variables

* **Concept name**: The name of the concept, equivalent to the name of the script
* **Concept label**: The label given to the output of the concept; concepts will appear in the output CSV as
  `CONCEPT_LABEL.CATEGORY`
* **Categories**: The actual categories for each concept that are identified
    * Each category will appear in the output CSV file as `CONCEPT_LABEL.CATEGORY` as the variable, and a count of
      occurences as the value

### History of Attempted Suicide

* Concept name: `suicide_attempt`
* Concept label: `SuicideAttempt`
* Concept definition: in specified note, had a suicide or self-harm attempt anytime in the past
* Categories:
    * `YES`: evidence for past attempt
    * `NO`: denied past attempt
    * `FAMILY`: past attempt associated with someone else (no necessarily family member)
    * `CODE`: attempt identified from ICD code
* Post-processing:
    * `C0455507`: History of attempted suicide
        * `A`: affirmative
        * `N`: negated
        * `X`: other subject (e.g., concept is relevant to a family member, not the patient)

### History of Smoking

* Concept name: `smoking`
* Concept label: `SmokingCategory`
* Concept definition: in specified note, evidence for current or historical smoking status
* Categories:
    * `NO`: no evidence for smoking
    * `CURRENT`: current evidence
    * `HISTORY`: historical evidence
    * `NEVER`: evidence for never smoking
    * `YES`: evidence for smoking
* Post-processing:
    * `C0337664`: Smoker - Persons with a history or habit of SMOKING
        * `A`: affirmed
        * `N`: negated
        * `H`: historical
    * `C0337672`: Non-smoker
        * `A`: affirmed
