# Migration Guide

- [Migration Guide](#migration-guide)
  - [Migrate to v1.0.0](#migrate-to-v100)
    - [Example config file (v1.1.2, INI):](#example-config-file-v112-ini)
  - [Migrate to v2.0.0](#migrate-to-v200)
    - [Example config file (v2.0.0, yaml):](#example-config-file-v200-yaml)
    - [TL;DR](#tldr)

## Migrate to v1.0.0

[Changelog](CHANGELOG.md#100---2022-05-29)

`todo` v1.0.0 added a new column `date_added` to the `todo` table of the todo database,

and you need to migrate your todo database to v1.0.0 if you were using a previous version.

Here's the how:

- Install [alembic](https://alembic.sqlalchemy.org/en/latest/), the database migration tool.
  ```bash
  pip install alembic # or method of your choice
  ``` 

- Run the migration scripts in this repository and fill the new column with the current time:
  ```bash
  # clone this repository
  git clone https://github.com/tddschn/todo-cli-tddschn.git
  cd todo-cli-tddschn

  # edit alembic.ini, change the sqlalchemy.url to your database url
  vim alembic.ini

  # migrate to new db schema
  python -m alembic revision --autogenerate -m "Initial Migration"
  python -m alembic upgrade head
  python -m alembic revision --autogenerate -m "Add date_added to Todo model"
  python -m alembic upgrade head

  # fill the new column (make sure to upgrade to v1.0.1 first)
  todo utils fill-date-added-column
  ```

### Example config file (v1.1.2, INI):
```ini
[General]
database = /Users/tscp/.todo-cli-tddschn.db # or anywhere you'd like

[Format]
# see https://strftime.org/ for the format specs
due_date = %%m-%%d
date_added = %%m-%%d
```

You can install this file with the following command:
```bash
curl -o "$(todo config path)" https://raw.githubusercontent.com/tddschn/todo-cli-tddschn/master/examples/config.ini
```

## Migrate to v2.0.0

[Changelog](CHANGELOG.md#200---2022-05-30)

`v2.0.0` uses `yaml` for the configuration file.

### Example config file (v2.0.0, yaml):
```yaml
database: "/Users/tscp/.todo-cli-tddschn.db" # or anywhere you'd like
format:
  # see https://strftime.org/ for the format specs
  due_date: "%m-%d"
  date_added: "%m-%d"
hide: # columns to hide for `ls` and `get` commands
  - "status"
  - "date_added"
  # - "id"
```

### TL;DR

You can install this file with the following command:
```bash
curl -o "$(todo config path)" https://raw.githubusercontent.com/tddschn/todo-cli-tddschn/master/examples/config.yaml
```
