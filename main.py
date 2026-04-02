import sys
import json
import os


def load_config(path: str = "config.json"):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: Configuration file '{path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"CRITICAL ERROR: '{path}' is not valid JSON.")
        sys.exit(1)


if __name__ == "__main__":
    config = load_config()

    # set up files and dirs
    quest_file = config.get("quest_file")
    inventory_file = config.get("inventory_file")
    reports_dir = config.get("repors_dir")
    processes_dir = config.get("processes_dir")

    print("--- Booting QuestLog System ---")
    print(f"Loaded Quest File Path: {quest_file}")
    print(f"Loaded Inventory File Path: {inventory_file}")
    print(f"Loaded Reports Directory Path: {reports_dir}")
    print(f"Loaded Processes Directory Path: {processes_dir}\n")
