#from QuestLogSystem.Quest import Quest
from QuestLogSystem.QuestLogManager import QuestLogManager
from typing import Callable, Any

class Cli:
    def __init__(self, manager: QuestLogManager, extra_commands: dict[str, Callable[...,Any]] = {}) -> None:
        self._manager = manager
        
        self._commands: dict[str, Callable[..., Any]] = {
            "plan": self._manager.plan,
            "quest gap": self._manager.gap,
            "quest complete": self._manager.complete_quest,
            "inventory add": self._manager.add_to_inventory,
            "inventory use": self._manager.use_from_inventory
        }
        
        self._commands |= extra_commands
        
    def read_line(self) -> str:
        """Reads a single line of input from the terminal."""
        try:
            return input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            #handle Ctrl+C or Ctrl+D
            return "exit"
    