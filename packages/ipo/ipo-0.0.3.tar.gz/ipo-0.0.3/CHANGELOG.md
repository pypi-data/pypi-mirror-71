# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.3] - 2020-06-15
### Added
- `recompose`
- `flat_enum`
- `intersperse`
- `grep`
- `grepo`

### Changed
- Change course: **we now wrap the data instead of each function**
- Rename `take` to `head`

### Removed
- Functions that were thin ipo wrappers around standard library functions:
	- `map` (use `map`)
	- `starmap` (use `itertools.starmap`)
	- `filter` (use `filter`)
	- `sort` (use `sorted`)
	- `str` (use `str`)
	- `list` (use `list`)
	- `dict` (use `dict`)
	- `islice` (use `itertools.islice`)
	- `takewhile` (use `itertools.takewhile`)
	- `enum` (use `enumerate`)
	- `join` (use `str.join`)
	- `items` (use `dict.items`)

## [0.0.2] - 2020-05-18
### Added
- Change log
- Examples in README
- `starmap`
- `islice` (= `ipo(itertools.islice)`)
- `read` to read files that aren't stdin

### Changed
- Rename `print` to `write` for symmetry with `read`

## [0.0.1] - 2020-05-18
### Added
- Route planning, liveboards and timeliness overview
- Published on PyPI
