# Changelog

All notable changes to this extension are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-20

### Added

- Read-only `inventory.py` extractor that regenerates every live `FR-`, `NFR-`, `SC-`, `AC-`, and `T-` ID from `spec.md` and `tasks.md` on each run and prints JSON.
- `speckit.speckit-inventory.list` command returning the complete inventory.
- `speckit.speckit-inventory.context` command returning a focused context pack for one task and the requirements it covers.
- Optional `before_specify` and `before_analyze` hooks.
