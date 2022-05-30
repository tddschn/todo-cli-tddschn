# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Pre 1.0.0] - 2022-04-22
### Added
- `todo` Commands: `a` for `add`, `rm` for `remove`, `m` for `modify`, `init` and `re-init`.
- Sub-commands: 
  - `ls` for todo listing, supports filtering and sorting based on `todo`'s properties.
  - `config` for getting and setting configuration.
  - `info` for getting info about the `todo`s.
- `INI` configuration file, supports setting custom todo database path.
- REST API of the `todo` app.

## [1.0.0] - 2022-05-29
### Added
- A new `todo` property: `date_added`.

    Requires manual migration with `alembic`, see [Migration Guide](migration.md#migrate-to-v100) for more info.

- `utils` sub-command: 
  - `export` todos to `todo add` commands that can be used for re-construct your todo database.
  - `fill-date-added-column` to fill `date_added` column of the `todo` table during migration

- `todo ls`: more filtering options, including `--due-date-before` and `--date-added-after`.

## [1.1.2] - 2022-05-29
### Added
- Custom date formatting
  - `--full-date-added` to display full date and time for the `ls` command
  - You can also specify date format strings in the config file.
### Changed
- Smarter default date formatting: Omits year if it's the current year.

## [2.0.0] - 2022-05-30
### Changed
- Change to use `yaml` config. [Migration Guide](migration.md#migrate-to-v200).

### Added
- Support hiding specific columns in the `ls` and `get` commands.