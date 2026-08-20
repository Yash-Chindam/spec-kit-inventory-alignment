# Changelog

All notable changes to this preset are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-20

### Added

- `wrap` override of `speckit.specify` adding a classify-against-the-inventory pre-pass (already-true / edit-existing / conflict / genuinely-new).
- `wrap` override of `speckit.analyze` that loads the complete live ID set as an input to cross-artifact coverage and conflict review.
- `append` override of `tasks-template` documenting the optional `covers:` field.
