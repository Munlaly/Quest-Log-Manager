import os
import sys
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import Main

# --- FIXTURES ---


@pytest.fixture
def mock_app(monkeypatch) -> Main:
    """
    Creates a Main application instance but intercepts the config loader
    """

    fake_config = {"processes_dir": "dummy_processes", "reports_dir": "dummy_reports"}
    monkeypatch.setattr(Main, "load_config", lambda path=None: fake_config)

    app = Main()

    app._manager = MagicMock()
    app._cli = MagicMock()

    return app


# --- TESTS ---


def test_load_config_valid_json(tmp_path):
    """Tests if load_config correctly parses a real JSON file."""
    # ARRANGE
    config_file = tmp_path / "config.json"
    config_file.write_text('{"reports_dir": "test_reports"}')

    # ACT
    config = Main.load_config(config_file)

    # ASSERT
    assert (
        config.get("reports_dir") == "test_reports"
    ), "The config loader must accurately parse and return the JSON dictionary."


def test_load_config_invalid_json_exits_program(tmp_path):
    """Tests if the program shuts down safely if the JSON is corrupted."""
    # ARRANGE
    bad_file = tmp_path / "bad_config.json"
    bad_file.write_text("{ this is not valid json }")

    # ACT & ASSERT
    with pytest.raises(SystemExit) as excinfo:
        Main.load_config(bad_file)

    assert (
        excinfo.value.code == 1
    ), "The system must exit with error code 1 if the config is invalid."


def test_exit_command_saves_inventory_and_closes(mock_app):
    """Tests that typing exit saves data before shutting down."""
    # ACT & ASSERT
    with pytest.raises(SystemExit) as excinfo:
        mock_app.exit()

    assert excinfo.value.code == 0, "The system must exit cleanly with code 0."
    assert (
        mock_app._manager.save_inventory.called
    ), "The system MUST call save_inventory before shutting down to prevent data loss."


def test_process_batch_commands_generates_report(mock_app, tmp_path, monkeypatch):
    """Tests the complex batch processor using Pytest's temporary directories."""
    # ARRANGE
    fake_process_dir = tmp_path / "processes"
    fake_reports_dir = tmp_path / "reports"
    fake_process_dir.mkdir()

    mock_app._config = {
        "processes_dir": str(fake_process_dir),
        "reports_dir": str(fake_reports_dir),
    }

    cmd_file = fake_process_dir / "test_commands.txt"
    cmd_file.write_text("plan\nexit")

    mock_app._cli.parse_line.return_value = ("plan", [])
    mock_app._cli.get_command.return_value = lambda: "Fake Plan Output"

    # ACT
    result = mock_app.process("test_commands.txt")

    # ASSERT
    assert (
        "successfully" in result
    ), "The process method should return a success message."

    expected_report = fake_reports_dir / "test_commands_report.txt"
    assert (
        expected_report.is_file()
    ), "The report file must be generated in the correct directory."

    report_content = expected_report.read_text()
    assert (
        "Fake Plan Output" in report_content
    ), "The returned values of commands must be printed into the report."
    assert (
        "--- End of Report ---" in report_content
    ), "The report must format correctly with headers and footers."
