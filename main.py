import sys
import json
from pathlib import Path
from typing import Callable, Any, NoReturn

from QuestLogSystem.QuestLogManager import QuestLogManager, Mode
from QuestLogSystem.Cli import Cli


class Main:
    def __init__(self):
        self._config: dict[str, str] = Main.load_config()

        self._manager: QuestLogManager = QuestLogManager(self._config)

        self._commands: dict[str, Callable[..., Any]] = {
            "exit": self.exit,
            "process": self.process,
        }

        self._cli: Cli = Cli(self._manager, self._commands)

    @staticmethod
    def load_config(path: Path = Path("config.json")) -> dict[str, str]:
        if not path.is_file():
            print(f"CRITICAL ERROR: Configuration file '{path}' not found or invalid.")
            return {}

        try:
            with open(path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"CRITICAL ERROR: Configuration file '{path}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"CRITICAL ERROR: '{path}' is not valid JSON.")
            sys.exit(1)

    def exit(self) -> NoReturn:
        """Saves inventory and coloses the program"""
        self._manager.save_inventory()
        sys.exit(0)

    def process(self, command_file_name: str) -> str:
        """Reads a file of commands, executes them, and logs the output to a report."""
        processes_dir = Path(self._config.get("processes_dir", ""))
        command_file = processes_dir / Path(command_file_name)
        if not command_file.is_file():
            print(f"Error: file '{command_file}' not found or does not exist!")
            return f"Process could not be executed"

        try:
            with open(command_file, "r") as f:
                commands: list[str] = f.read().splitlines()

        except IOError as e:
            print(f"Error reading file: {e}")
            return f"Process could not be executed"

        reports_dir = Path(self._config.get("reports_dir", ""))
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = reports_dir / f"{command_file.stem}_report.txt"

        original_stdout = sys.stdout

        print(f"Processing file {command_file} ...")

        try:
            with open(report_path, "w") as f:
                sys.stdout = f

                for line_num, raw_cmd in enumerate(commands, 1):
                    if raw_cmd.strip() == "":
                        continue

                    print(f"\n[Line {line_num}] Executing: {raw_cmd}")

                    cmd_name, args = self._cli.parse_line(raw_cmd)

                    if not cmd_name:
                        continue

                    handler = self._cli.get_command(cmd_name)

                    if handler:
                        try:
                            result = handler(*args)
                            if result is not None:
                                print(result)
                        except TypeError:
                            print(f'Error: Invalid arguments for command "{cmd_name}"')
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        print(f"Unknown command: '{cmd_name}'")

                print("\n--- End of Report ---")
                return f"Process executed successfully"
        except IOError as e:
            sys.stdout = original_stdout
            print(f"Error generating report: {e}")
            return f"Process could not be executed"
        finally:
            sys.stdout = original_stdout

    def run(self) -> None:
        """Runs the main application logic"""
        # main logic
        print("--- Booting QuestLog System ---")

        # parse and execute first terminal command
        if len(sys.argv) > 1:
            initial_input = " ".join(sys.argv[1:])

            command_name, args = self._cli.parse_line(initial_input)

            handler = self._cli.get_command(command_name)
            if handler:
                try:
                    result = handler(*args)

                    if result is not None:
                        print(result)

                except TypeError:
                    print(f'Invalid arguments for command "{command_name}"')

                except Exception as e:
                    print(e)
            else:
                print(f"Unknown command: {command_name}")

        if self._manager.mode == Mode.INTERACTIVE:
            while True:
                raw_input = self._cli.read_line()

                if not raw_input:
                    continue

                command_name, args = self._cli.parse_line(raw_input)

                handler = self._cli.get_command(command_name)

                if handler:
                    try:
                        result = handler(*args)

                        if result is not None:
                            print(result)

                    except TypeError:
                        print(f'Invalid arguments for command "{command_name}"')

                    except Exception as e:
                        print(e)

                else:
                    print(f"Unknown command: {command_name}")


if __name__ == "__main__":
    app = Main()
    try:

        app.run()
    except Exception as e:
        print(e)

        sys.exit(1)
