#!/usr/bin/env python3

from .cli import app
import typer
from typer.testing import CliRunner
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()

session = PromptSession()
runner = CliRunner()

registered_command_names = [x.name for x in app.registered_commands]
registered_group_names = [x.name for x in app.registered_groups]

from prompt_toolkit.completion import WordCompleter

# html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
# text = prompt('Enter HTML: ', completer=html_completer)

command_completer = WordCompleter(
    list(filter(None, (registered_command_names + registered_group_names)))
)


@bindings.add('c-t')
def _(event):
    "Exit when `c-d` is pressed."
    event.app.exit()


def main() -> None:
    while True:
        text = session.prompt(
            "todo> ", auto_suggest=AutoSuggestFromHistory(), completer=command_completer
        )
        # print('You said: %s' % text)
        result = runner.invoke(app, text, color=True)
        typer.secho(result.output)


if __name__ == "__main__":
    main()
