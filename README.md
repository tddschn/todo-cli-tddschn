# todo-cli-tddschn

A simple command-line Todo app with typer and sqlite

- [todo-cli-tddschn](#todo-cli-tddschn)
	- [Install](#install)
		- [pipx (recommended)](#pipx-recommended)
		- [pip](#pip)
	- [Usage](#usage)
		- [todo](#todo)
		- [todo config](#todo-config)
		- [todo ls](#todo-ls)
	- [SQLite database schema](#sqlite-database-schema)
	- [Screenshots](#screenshots)

## Install

### pipx (recommended)
```
pipx install todo-cli-tddschn
```

### pip
```
pip install todo-cli-tddschn
```

## Usage

### todo
```
todo --help

Usage: todo [OPTIONS] COMMAND [ARGS]...

  tddschn's command line todo app

Options:
  -v, --version         Show the application's version and exit.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  a        Add a new to-do with a DESCRIPTION.
  clear    Remove all to-dos.
  config   Getting and managing the config
  g        Get a to-do by ID.
  info     Get infos about todos
  init     Initialize the to-do database.
  ls       list all to-dos, ordered by priority and due date.
  m        Modify a to-do by setting it as done using its TODO_ID.
  re-init  Re-initialize the to-do database.
  rm       Remove a to-do using its TODO_ID.
```
### todo config
```
todo config --help

Usage: todo config [OPTIONS] COMMAND [ARGS]...

  Getting and managing the config

Options:
  --help  Show this message and exit.

Commands:
  db-path  Get the path to the to-do database.
  edit     Edit the config file.
  path     Get the path to the config file.
```

### todo ls
```
todo ls --help

Usage: todo ls [OPTIONS] COMMAND [ARGS]...

  list all to-dos, ordered by priority and due date.

Options:
  -d, --description TEXT
  -p, --priority [low|medium|high]
  -s, --status [todo|done|deleted|cancelled|wip]
  -pr, --project TEXT
  -t, --tags TEXT
  -dd, --due-date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
  --help                          Show this message and exit.

Commands:
  project  Filter to-dos by project.
  tag      Filter to-dos by tag.
```
## SQLite database schema

![schema](images/diagram.png)

## Screenshots

![screenshot](images/screenshot.png)

![screenshot-2](images/screenshot-2.png)