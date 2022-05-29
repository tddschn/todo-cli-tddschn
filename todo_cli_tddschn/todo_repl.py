#!/usr/bin/env python3

from .cli import app
from click_repl import register_repl


register_repl(app)

if __name__ == '__main__':
    app()
