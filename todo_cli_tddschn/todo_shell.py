#!/usr/bin/env python3

from prompt_toolkit import prompt


def main() -> None:
    answer = prompt('Give me some input: ')
    print('You said: %s' % answer)


if __name__ == '__main__':
    main()
