#from QuestLogSystem.Quest import Quest
from QuestLogSystem.QuestLogManager import QuestLogManager
from typing import Callable, Any
import shlex

class Cli:
    def __init__(self, manager: QuestLogManager, extra_commands: dict[str, Callable[...,Any]]| None = None) -> None:
        self._manager = manager
        
        self._commands: dict[str, Callable[..., Any]] = {
            "plan": self._manager.plan,
            "quest gap": self._manager.gap,
            "quest complete": self._manager.complete_quest,
            "quest list": self._list_quests,
            "inventory add": self._manager.add_to_inventory,
            "inventory use": self._manager.use_from_inventory,
            "manage": self._manager.set_to_interactive
        }
        if extra_commands is not None:
            self._commands |= extra_commands
    @staticmethod    
    def read_line() -> str:
        """Reads a single line of input from the terminal."""
        try:
            return input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            #handle Ctrl+C or Ctrl+D
            return "exit"
        
    def parse_line(self, line: str) -> tuple[str, list[Any]]:
        """
        Parses raw text into a command string and a list of arguments.
        Handles quoted strings and converts numbers to integers.
        """
        if not line:
            return "", []
        
        try:
            parts = shlex.split(line)
            
        except ValueError as e:
            print(f"Syntax Error: {e}") 
            return "", []
        
        if not parts:
            return "", []
        
        command_name = ""
        args_raw = []
        
        if len(parts) >= 2:
            potential_two_word = f"{parts[0]} {parts[1]}".lower()
            if potential_two_word in self._commands:
                command_name = potential_two_word
                args_raw = parts[2:]
                
            else:
                command_name = parts[0]
                args_raw = parts[1:]
                
        else:
                command_name = parts[0]
                args_raw = parts[1:]
                
        args_final: list[Any] = []
        for arg in args_raw:
            try:
                args_final.append(int(arg))
            except ValueError:
                #append str arg in lowercase
                args_final.append(arg.lower())
                
        return command_name, args_final
    
    def get_command(self, cmd_name: str) -> Callable[..., Any] | None:
        """Safely fetches the function from the commands dict."""
        return self._commands.get(cmd_name)
    
    def _list_quests(self) -> str:
        """Helper method to fetch and format the quest list."""
        quest_dict = self._manager.quests 
        
        if not quest_dict:
            return "No quests currently loaded."
            
        formatted_quests = [str(quest) for quest in quest_dict.values()]
        return "\n\n".join(formatted_quests)
        