import json
from Inventory import Inventory
from Quest import Quest


class QuestLogManager:
    def __init__(self, paths: dict[str, str]) -> None:
        # get file and dir paths
        self._quest_file = paths.get("quest_file")
        self._inventory_file = paths.get("inventory_file")
        self._reports_dir = paths.get("reports_dir")
        self._processes_dir = paths.get("processes_dir")

        self._inventory: Inventory = Inventory(
            QuestLogManager._load_inventory(self._inventory_file)
        )

        self._quests: dict[str, Quest] = QuestLogManager._load_quests(self._quest_file)

    # helpers
    @staticmethod
    def _load_inventory(path: str) -> dict[str, int]:
        try:
            with open(path, "r") as file:
                return json.load(file)

        except FileNotFoundError as e:
            print(f"CRITICAL ERROR: Inventory file '{path}' not found.")
            return {}
        except json.JSONDecodeError as e:
            print(f"CRITICAL ERROR: '{path}' is not valid JSON.")
            return {}

    @staticmethod
    def _load_quests(path: str) -> dict[str, Quest]:
        quests_dict: dict[str, Quest] = {}
        try:
            with open(path, "r") as file:
                # parse JSON array into a list of dicts
                quest_data_list = json.load(file)

                for q_dict in quest_data_list:
                    name = q_dict.get("name")
                    items = q_dict.get("items", {})

                    new_quest = Quest(name, items)

                    # store the names in lowercase for easy lookups
                    name = name.strip().lower()
                    quests_dict[name] = new_quest

            return quests_dict

        except FileNotFoundError:
            print(f"CRITICAL ERROR: Quest file '{path}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"CRITICAL ERROR: '{path}' is not valid JSON.")
            return {}

    def _is_quest_completable(self, quest: Quest) -> bool:
        for name, cnt in quest.items.items():
            if not self._inventory.is_available(name, cnt):
                return False
        return True

    def _save_inventory(self):
        """Saves the current inventory state back to the JSON file."""
        try:
            with open(self._inventory_file, "w") as f:
                json.dump(self._inventory.items, f, indent=4)

        except IOError as e:
            print(f"ERROR: Failed to save inventory to '{self._inventory_file}'.")
            print(f"Details: {e}")

    # callable methods
    def plan(self) -> list[str]:
        """Filters and returns a list of only completable quests."""
        return [
            quest.name
            for quest in self._quests.values()
            if self._is_quest_completable(quest)
        ]

    def complete_quest(self, quest: Quest):
        """Consumes inventory items to complete a quest if possible."""
        if not self._is_quest_completable(quest):
            raise ValueError(
                f"Quest '{quest.name}' is not completable. Missing required items."
            )

        # update inventory
        for item, cnt in quest.items.items():
            self._inventory.use_item(item, cnt)

        self._save_inventory()

    def add_to_inventory(self, name: str, cnt: int):
        """Adds item to inventory and saves the state."""
        self._inventory.add_item(name, cnt)
        self._save_inventory()

    def use_from_inventory(self, name: str, cnt: int):
        """Removes item from inventory and saves the state."""
        self._inventory.use_item(name, cnt)
        self._save_inventory()
