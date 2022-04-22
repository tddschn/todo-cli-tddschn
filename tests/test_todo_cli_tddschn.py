import os
import tempfile
from todo_cli_tddschn import __version__, __app_name__
from todo_cli_tddschn.cli import app

from typer.testing import CliRunner

# runner = CliRunner()


class TestTodo:

    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()
        cls.db_path = tempfile.mkstemp(suffix=".db")[1]

    @classmethod
    def teardown_class(cls):
        os.unlink(cls.db_path)

    def test_version(self):
        result = self.runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert f"{__app_name__} v{__version__}\n" == result.output