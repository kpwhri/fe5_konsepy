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
  * `python src/run_concept.py --input-files sample/corpus.csv --outdir out --id-label studyid --concept suicide_attempt`

If you need to specify different headers/variables/labels to your corpus file, use the following command line arguments (the defaults are shown):
* `--id-label studyid`
* `--noteid-label note_id`
* `--notedate-label note_date`
* `--notetext-label note_text`

## Variables

### History of Attempted Suicide

* Concept name: `suicide_attempt`
* Categories:
    * `YES`: evidence for past attempt
    * `NO`: denied past attempt
    * `FAMILY`: past attempt associated with someone else (no necessarily family member)
    * `CODE`: attempt identified from ICD code

### History of Smoking

* Concept name: `smoking`
* Categories:
    * `NO`: no evidence for smoking
    * `CURRENT`: current evidence
    * `HISTORY`: historical evidence
    * `NEVER`: evidence for never smoking
    * `YES`: evidence for smoking
