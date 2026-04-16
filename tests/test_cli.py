import os
import sys
import io
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from QuestLogSystem.Cli import Cli
from QuestLogSystem.QuestLogManager import QuestLogManager


@pytest.fixture
def cli_instance() -> Cli:
    """Creates a mock Cli instance for every test"""
    fake_manager: MagicMock = MagicMock()

    cli = Cli(fake_manager)

    return cli


def test_read_line_reading(monkeypatch):
    # ARRANGE
    fake_terminal_input = io.StringIO("   testing line reading   \n")
    monkeypatch.setattr("sys.stdin", fake_terminal_input)

    # ACT
    line = Cli.read_line()

    # Assert
    assert line == "testing line reading", "Leading and ending spaces must be ignored"


def test_read_line_err(monkeypatch):
    # ARRANGE
    def mock_input_crash(prompt: str = ""):
        raise KeyboardInterrupt()

    monkeypatch.setattr("builtins.input", mock_input_crash)

    # ACT
    line = Cli.read_line()

    # Assert
    assert line == "exit", "Must return exit command for interrupt CTRL + C"


def test_parse_line_one_word_command(cli_instance):
    # ACT
    cmd_name, args = cli_instance.parse_line("plan")

    # ASSERT
    assert cmd_name == "plan", "Command names must be standardized to lowercase"
    assert args == [], "No arguments for command plan"


def test_parse_line_two_word_command_with_mixed_args(cli_instance):
    # ACT
    cmd_name, args = cli_instance.parse_line('inventory add "Health Potion" 5')

    # ASSERT
    assert (
        cmd_name == "inventory add"
    ), "Command names must be standardized to lowercase"
    assert args[0] == "health potion", "Names must be standardized to lowercase"
    assert args[1] == 5, "Number argument must be number"


def test_parse_line_ignores_extra_spaces(cli_instance):
    # ACT
    cmd_name, args = cli_instance.parse_line("   manage   ")

    # ASSERT
    assert cmd_name == "manage"
    assert args == [], "Leading and ending spaces must be ignored"


def test_parse_line_empty_string(cli_instance):
    # ACT
    cmd_name, args = cli_instance.parse_line("")

    # ASSERT
    assert cmd_name == ""
    assert args == [], "Empty line must be ignores"
