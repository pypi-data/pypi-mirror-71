# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2020-06-12
### Added
- `CHANGELOG.md`
- Repository URL in `pyproject.toml`.

### Changed
- Refactor `SteppedAugustus._cipher` to a generalized, easy to modify, and lazy algorithm.
- Refactor `SteppedAugustus._cipher` to include tabs and newlines.
- Refactor `SteppedAugustus.right_cipher` and `SteppedAugustus.left_cipher` in accordance to
  the change in `SteppedAugustus._cipher`.
- Refactor documentation.
- Fix typo in `README.md`.
- Fix rouge character in `README.md`.
- Fix formatting of Suetonius' quote in `README.md`.

## [1.0.0] - 2020-06-11
### Added
- `SteppedAugustus` class interface that implements the functionality from the original
  proof of concept through the `_cipher` method, and the `right_cipher` and `left_cipher`
  properties.
- Availability through PyPI.

### Changed
- Use the `SteppedAugustus` interface for the command-line application.

### Removed
- Initial proof of concept module.

## [0.0.0] - 2020-06-11
### Added
- Initial proof of concept module.
- Initial command-line application.
