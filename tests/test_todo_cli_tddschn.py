from todo_cli_tddschn import __version__, __app_name__
from todo_cli_tddschn.cli import app

from typer.testing import CliRunner

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" == result.output