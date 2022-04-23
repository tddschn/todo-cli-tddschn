import os
from pathlib import Path
import tempfile
from todo_cli_tddschn import __version__, __app_name__
from todo_cli_tddschn.cli import app
from todo_cli_tddschn.config import get_config_path, get_database_path

from typer.testing import CliRunner

# runner = CliRunner()


class TestTodo:

    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()
        # cls.config_file_path = tempfile.mkstemp(suffix='.ini')[1]
        # cls.db_path = tempfile.mkstemp(suffix=".db")[1]
        cls.config_file_path = get_config_path()
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

    def test_add(self):
        result = self.runner.invoke(
            app, ['a', 'test', '--priority', 'low', '--project', 'test'])
        assert result.exit_code == 0
        # assert "Added to-do successfully" in result.output

    def test_modify(self):
        result = self.runner.invoke(
            app, ['m', '1', '-d', 'test modified', '--priority', 'high'])
        assert result.exit_code == 0
        # assert "Added to-do successfully" in result.output

    def test_re_init(self):
        # result = self.runner.invoke(app, [
        #     're-init', '--db-path', self.db_path, '--config-file-path',
        #     self.config_file_path
        # ],
        #                             input='y\n')
        result = self.runner.invoke(app, ['re-init'], input='\ny\n')
        assert result.exit_code == 0
        assert "Database created successfully" in result.output