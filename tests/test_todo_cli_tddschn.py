import os
from pathlib import Path
import sys
import tempfile
from todo_cli_tddschn import __version__, __app_name__
from todo_cli_tddschn.cli import app, _check_db_exists
from todo_cli_tddschn.config import get_config_path, get_database_path

from typer.testing import CliRunner
import pytest

# runner = CliRunner()


def with_func(func):

    def with_list(method):

        def wrapper(self, *args, **kwargs):
            method(self, *args, **kwargs)
            func(self)

        return wrapper

    return with_list


class TestTodo:

    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()
        # cls.config_file_path = tempfile.mkstemp(suffix='.ini')[1]
        # cls.db_path = tempfile.mkstemp(suffix=".db")[1]
        cls.config_file_path = get_config_path()
        if not _check_db_exists():
            cls.teardown_class()
        cls.db_path = get_database_path(Path(cls.config_file_path))

    @classmethod
    def teardown_class(cls):
        os.unlink(cls.db_path)

    def test_version(self):
        result = self.runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert f"{__app_name__} v{__version__}\n" == result.output

    def test_init(self):
        result = self.runner.invoke(app, ['init'], input='\n')
        # result = self.runner.invoke(app, [
        #     "init", "--db-path", self.db_path, '--config-file-path',
        #     self.config_file_path
        # ])
        assert result.exit_code == 0
        assert "Database created successfully" in result.output

    @pytest.mark.parametrize('cmd', [([
        'finish', 'cooking', 'eva', '-dd', '2121-12-11', '-pr', 'eva', '-s',
        'wip'
    ]), (['eat', 'eva', '-p', 'high', '-t', 'lol', '-t', 'dinner']),
                                     (['test'])])
    def test_add(self, cmd):
        result = self.runner.invoke(app, ['a', *cmd])
        assert result.exit_code == 0
        # assert "Added to-do successfully" in result.output

    def test_list(self):
        result = self.runner.invoke(app, ['ls'])
        assert result.exit_code == 0
        print(result.output, file=sys.stderr)
        # assert "Added to-do successfully" in result.output

    # @with_func(self.test_list)
    def test_modify(self):
        result = self.runner.invoke(
            app, ['m', '1', '-d', 'test modified', '--priority', 'high'])
        assert result.exit_code == 0
        # assert "Added to-do successfully" in result.output

    def test_list2(self):
        result = self.runner.invoke(app, ['ls'])
        assert result.exit_code == 0
        print(result.output, file=sys.stderr)

    def test_remove(self):
        result = self.runner.invoke(app, ['rm', '1'])
        assert result.exit_code == 1

    def test_remove2(self):
        result = self.runner.invoke(app, ['rm', '1'], input='y\n')
        assert result.exit_code == 0

    def test_list3(self):
        result = self.runner.invoke(app, ['ls'])
        assert result.exit_code == 0
        print(result.output, file=sys.stderr)

    def test_clear(self):
        result = self.runner.invoke(app, ['clear'], input='y\n')
        assert result.exit_code == 0

    def test_info_count(self):
        result = self.runner.invoke(app, ['info', 'count'])
        assert result.exit_code == 0
        assert "Total todos: 0" in result.output

    def test_re_init(self):
        # result = self.runner.invoke(app, [
        #     're-init', '--db-path', self.db_path, '--config-file-path',
        #     self.config_file_path
        # ],
        #                             input='y\n')
        result = self.runner.invoke(app, ['re-init'], input='\ny\n')
        assert result.exit_code == 0
        assert "Database created successfully" in result.output