# Changelog
All notable changes to this project will _likely_ be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Reference

Types of changes:

* `Added`: for new features.
* `Changed`: for changes in existing functionality.
* `Deprecated`: for soon-to-be removed features.
* `Removed`: for now removed features.
* `Fixed`: for any bug fixes.
* `Security`: in case of vulnerabilities.

## [Unreleased]


## [0.0.4] - 2024-11-18

### Added

* Logging file for postprocessing, tests
* Improved handling of other subject (e.g., disallowing across period-delimited sentence boundary)
* Handling postprocessing using derived classes to improve code reuse
* Try to identify the `output.jsonl` file and parse it to create the feature details file
* Added flag to replace control characters with '?' in the matched text field (FEATURE_DETAILS table)


## [0.0.3] - 2024-09-25

### Added

* Postprocessing for both smoking and suicide attempt
* Improved instructions specific to FE5 work

### Changed

* Handle suggestion to quit smoking as current smoker
* Handle family history section for suicide attempt (but not long-range)
* Allowed increased complexity for historical time frame (suicide attempt) 

### Fixed

* Added missing argumnets


## [0.0.2] - 2024-05-29

### Fixed

* Handle where getting text snippets returned True rather than skipping
* Fix 'Smoking status: never assessed'
* Fix hypothetical/questions sentences
* Account for other subject (e.g., family)

## [0.0.1] - 2024-01-12

### Added

* Added smoking history
* Added history of attempted suicide
* Added icd codes
* Added problem list to demonstrate when item appears to be in the problem list 
* Expanded `get_context` to reset context when searching the context of match
* Expanded predicate for SAs: age, x times, as a teen with tests
* Added 'self-harm behavior' to SA with tests

### Fixed

* Handle post-negation
* Handle other subject/non-patient references
* Improved handling of other subject
* Don't take preceding 'denied' if preceded by colon
* Reordered regexes to handle 'denies hx of SA in college'

[unreleased]: https://github.com/kpwhri/fe5_konsepy/compare/0.0.3...HEAD
[0.0.4]: https://github.com/kpwhri/fe5_konsepy/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/kpwhri/fe5_konsepy/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/kpwhri/fe5_konsepy/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/kpwhri/fe5_konsepy/releases/0.0.1