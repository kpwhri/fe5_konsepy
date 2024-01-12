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

### Fixed

* Handle where getting text snippets returned True rather than skipping

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
