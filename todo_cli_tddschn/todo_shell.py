#!/usr/bin/env python3

from .cli import app
import typer
from typer.testing import CliRunner
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

session = PromptSession()
runner = CliRunner()


def main() -> None:
    while True:
        text = session.prompt('todo> ', auto_suggest=AutoSuggestFromHistory())
        # print('You said: %s' % text)
        result = runner.invoke(app, text, color=True)
        typer.secho(result.output)


if __name__ == '__main__':
    main()
