import sys
import json 
from pathlib import Path
from typing import Callable, Any

from QuestLogSystem.QuestLogManager import QuestLogManager, Mode
from QuestLogSystem.Cli import Cli

class Main:
    def __init__(self):
        self._config: dict[str,str] = Main.load_config()
    
        self._manager:QuestLogManager = QuestLogManager(self._config)
        
        self._commands: dict [ str, Callable[..., Any] ] = {
            'exit' : self.exit
            }
        
        self._cli: Cli = Cli(self._manager, self._commands)
        
    @staticmethod
    def load_config(path: Path = Path("config.json")) -> dict[str,str]:
        if not path.is_file():
                print(f"CRITICAL ERROR: Inventory file '{path}' not found or invalid.")
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
        
    def exit(self) -> str:
        self._manager.save_inventory()
        sys.exit(0)
        
 

            
    def run(self)->None:
        '''Runs the main application logic'''
        #main logic
        print("--- Booting QuestLog System ---")
        
        #parse and execute first terminal command
        if len(sys.argv) > 1:
            initial_input = " ".join(sys.argv[1:])
            
            command_name, args = self._cli.parse_line(initial_input) 
            
            handler =  self._cli.get_command(command_name)
            if handler:
                try:
                    result = handler(*args)
                        
                    if result is not None:
                        print(result)
                
                except TypeError:
                    print(f'Invalid arguments for command \"{command_name}\"')
                                
                except Exception as e:
                        print(e)
            else:
                print(f'Unknown command: {command_name}')
        
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
                        print(f'Invalid arguments for command \"{command_name}\"')
                            
                    except Exception as e:
                        print(e)
                        
                else:
                    print(f'Unknown command: {command_name}')



if __name__ == "__main__":
    app = Main()
    try:
       
        app.run()
    except Exception as e:
       print(e)
       
       sys.exit(1)