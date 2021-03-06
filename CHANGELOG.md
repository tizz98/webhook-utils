# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.2] - 2021-12-30
### Added
- End-to-end FastAPI examples

### Fixed
- Fixed `WebhookAuth` signature generation method call parameter order

## [0.3.1] - 2021-12-30
### Removed
- Remove erroneous `print` in `httpx_auth.py`

### Added
- Add `flake8-print` to check for `print` statements

## [0.3.0] - 2021-12-29
### Added
- `WebhookRouter` for `FastAPI` users to extend `APIRouter` with built-in webhook signature validation
- Upload coverage report to [Codecov](https://codecov.io/)

## [0.2.0] - 2021-12-29
### Added
- `WebhookAuth` injects signed request body as a header for `httpx`

## [0.1.0] - 2021-12-29
### Added
- Initial release.
- Crypto module with support for generating and verifying signatures.
