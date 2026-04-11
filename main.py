import sys
import json 
from pathlib import Path

from QuestLogSystem.QuestLogManager import QuestLogManager, Mode
from QuestLogSystem.Cli import Cli



def load_config(path: Path = Path("config.json")) -> dict[str,str]:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: Configuration file '{path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"CRITICAL ERROR: '{path}' is not valid JSON.")
        sys.exit(1)
        
 

            
def run()->None:
    '''Runs the main application logic'''
    config: dict[str,str] = load_config()
    
    # set up files and dirs
    quest_file: Path = Path(config.get("quest_file", ""))
    inventory_file: Path = Path(config.get("inventory_file", ""))
    reports_dir: Path = Path(config.get("reports_dir",""))
    processes_dir: Path = Path(config.get("processes_dir",""))
    
    manager:QuestLogManager = QuestLogManager(config)
    
    #sub functions
    def exit()->None:
        manager.save_inventory()
        sys.exit(0)
        
    cli: Cli = Cli(manager, {"exit": exit})
    print(cli)
   
    print("--- Booting QuestLog System ---")
    print(f"Loaded Quest File Path: {quest_file}")
    print(f"Loaded Inventory File Path: {inventory_file}")
    print(f"Loaded Reports Directory Path: {reports_dir}")
    print(f"Loaded Processes Directory Path: {processes_dir}\n")

    #parese and execute first terminal argument
    
    if manager.mode == Mode.INTERACTIVE:
        while True:
            line = cli.read_line()
            print(line)



if __name__ == "__main__":
    try:
        run()
    except Exception as e:
       print(e)
       
       sys.exit(1)