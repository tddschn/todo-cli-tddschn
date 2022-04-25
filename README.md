# todo-cli-tddschn

A simple command-line Todo app made with typer, sqlite and REST API.

- [todo-cli-tddschn](#todo-cli-tddschn)
	- [Features](#features)
	- [Install](#install)
		- [pipx (recommended)](#pipx-recommended)
		- [pip](#pip)
	- [Usage](#usage)
		- [todo](#todo)
		- [todo ls](#todo-ls)
		- [todo serve](#todo-serve)
		- [todo config](#todo-config)
		- [todo info](#todo-info)
	- [Why do you made this?](#why-do-you-made-this)
	- [SQLite database schema](#sqlite-database-schema)
	- [Screenshots](#screenshots)

## Features
- Creating, reading, updating, and deleting todos;
- Nicely formatting the outputs (with color);
- `todo ls` lists all todos, ordered by priority and due date, the todos without a due date are put last (nullslast).
- Not only the command line interface - you can also CRUD your todos by making HTTP requests to the [REST API](#todo-serve).

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

You can add, modify, or remove (all) todos with the `todo` command:

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

### todo ls

List and filter the todos.

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

### todo serve

Serve the REST API (built with FastAPI)

```
todo serve --help
Usage: todo serve [OPTIONS]

  serve REST API. Go to /docs for interactive documentation on API usage.

Options:
  --host TEXT       [default: 127.0.0.1]
  --port INTEGER    [default: 5000]
  --log-level TEXT  [default: info]
  --help            Show this message and exit.
```

### todo config

Get or edit the configurations

```
todo config --help

Usage: todo config [OPTIONS] COMMAND [ARGS]...

  Getting and managing the config

Options:
  --help  Show this message and exit.

Commands:
  db-path  Get the path to the to-do database.
  edit     Edit the config file. # Opens in default editor
  path     Get the path to the config file.
```

### todo info

Get the info and stats about the todos.

```
todo info --help

Usage: todo info [OPTIONS] COMMAND [ARGS]...

  Get infos about todos

Options:
  --help  Show this message and exit.

Commands:
  count  Get todo counts
```


## Why do you made this?

For practicing my python and SQL skills.

If you're looking for an awesome CLI todo app, try [taskwarrior](https://taskwarrior.org/).
## SQLite database schema

![schema](images/diagram.png)

## Screenshots

![screenshot](images/screenshot.png)

![screenshot-2](images/screenshot-2.png)

![todo-serve](images/todo-serve.png)

![api-docs](images/api-docs.png)