# Changelog

### Changed
- Add Django 4.1 support
- Confirm Python 3.11 support

### Fixed
- Fix datetime parsing problem in ``JDateTimeField``

## [6.0.0] - 2022-02-21
### Changed
- Update install_requires to use ``jdatetime>=4.0.0``
- Drop Python 3.6 support

## [5.1.0] - 2022-01-30
- Add support for `__date` lookup filter

### Changed
- Remove deprecated `datetime_safe` and use `sanitize_strftime_format`

## [5.0.0] - 2021-12-21
### Changed
- Add Python 3.10 support
- Add Django 4.0 support
- Drop Django < 3.2 support

## [4.3.0] - 2021-07-01
- Add DRF serializer field for JDateTimeField
### Changed
- Drop Python 3.5 support

## [4.2.0] - 2021-06-08
- Add DRF serializer field for JDateField
### Changed
- Drop Django 3.0 support
- Add Django 3.2 support

## [4.1.2] - 2020-12-21
### Fixed
- Fix chaining filters problem

## [4.1.1] - 2020-12-16
### Fixed
- Fixed `jDateTimeField` problem with `auto_now_add` when tz enable (#124)

## [4.1.0] - 2020-12-11
### Fixed
- Fix Django Jalali javascipt files loading when Django Jquery file loaded first

### Changed
- Add Python 3.9 support
- Drop Python 3.4 support
- Drop Django < 2.2 support

## [4.0.0] - 2020-06-22
### Changed
- Improved handling timezone

## [3.4.0] - 2020-06-17
### Fixed
- Fix serialization of django_jalali.db.models

