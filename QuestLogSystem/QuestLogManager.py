import json
from pathlib import Path
from QuestLogSystem.Inventory import Inventory
from QuestLogSystem.Quest import Quest
from enum import Enum


class Mode(Enum):
    DEFAULT = 1
    INTERACTIVE = 2


class QuestLogManager:
    def __init__(self, paths: dict[str, str], mode: Mode = Mode.DEFAULT) -> None:
        # get file and dir paths
        self._quest_file: Path = Path(paths.get("quest_file", ""))
        self._inventory_file: Path = Path(paths.get("inventory_file", ""))
        self._reports_dir: Path = Path(paths.get("reports_dir", ""))
        self._processes_dir: Path = Path(paths.get("processes_dir", ""))

        self._mode = mode

        self._inventory: Inventory = Inventory(
            QuestLogManager.load_inventory(self._inventory_file)
        )

        self._quests: dict[str, Quest] = QuestLogManager.load_quests(self._quest_file)

    def __repr__(self) -> str:
        result: list[str] = []

        result.append(f"Current mode: {self._mode}")
        result.append(f"Inventory: {repr(self._inventory)}")
        result.append("Quests:")
        result.extend([repr(q) for q in self._quests.values()])

        return "\n".join(result)

    # helpers
    @staticmethod
    def load_inventory(path: Path) -> dict[str, int]:
        """Loads nventory from json file"""
        if not path.is_file():
            print(f"CRITICAL ERROR: Inventory file '{path}' not found or invalid.")
            return {}

        try:
            with open(path, "r") as file:
                return json.load(file)

        except FileNotFoundError:
            print(f"CRITICAL ERROR: Inventory file '{path}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"CRITICAL ERROR: '{path}' is not valid JSON.")
            return {}

    @staticmethod
    def load_quests(path: Path) -> dict[str, Quest]:
        """Loads the quests from the quest file"""
        if not path.is_file():
            print(f"CRITICAL ERROR: Quest file '{path}' not found or invalid.")
            return {}

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

    # private methods
    def _is_quest_completable(self, quest: Quest) -> bool:
        for name, cnt in quest.items.items():
            if not self._inventory.is_available(name, cnt):
                return False
        return True

    # public methods
    def save_inventory(self) -> None:
        """Saves the current inventory state back to the JSON file."""
        try:
            with open(self._inventory_file, "w") as f:
                json.dump(self._inventory.items, f, indent=4)

        except IOError as e:
            print(f"ERROR: Failed to save inventory to '{self._inventory_file}'.")
            print(f"Details: {e}")

    def complete_quest(self, quest_name: str) -> str:
        """Consumes inventory items to complete a quest if possible."""
        quest: Quest | None = self.quests.get(quest_name)
        if quest is None:
            raise ValueError(f"Quest: {quest_name} does not exist")
        if not self._is_quest_completable(quest):
            raise ValueError(
                f"Quest '{quest.name}' is not completable. Missing required items."
            )

        # update inventory
        for item, cnt in quest.items.items():
            self._inventory.use_item(item, cnt)

        self.save_inventory()

        return f'Quest "{quest_name}" successfully completed!'

    def add_to_inventory(self, name: str, cnt: int) -> str:
        """
        Adds item to inventory and saves the state.
        Errors will bubble up.
        """
        self._inventory.add_item(name, cnt)
        self.save_inventory()
        return f"{cnt} {name} added!"

    def use_from_inventory(self, name: str, cnt: int) -> str:
        """
        Removes item from inventory and saves the state.
        Errors will bubble up.
        """
        self._inventory.use_item(name, cnt)
        self.save_inventory()
        return f"{cnt} {name} used!"

    def plan(self) -> list[str]:
        """Filters and returns a list of only completable quests."""
        return [
            quest.name
            for quest in self._quests.values()
            if self._is_quest_completable(quest)
        ]

    def gap(self, quest_name: str) -> dict[str, int]:
        """Performs the gap analysis"""
        clean_name = quest_name.strip().lower()

        if clean_name not in self._quests:
            raise ValueError(f"Quest with name: {clean_name} does not exist")

        missing: dict[str, int] = {}
        target_quest = self._quests[clean_name]
        for name, cnt in target_quest.items.items():
            current_cnt = self._inventory.get_item_count(name)
            if cnt > current_cnt:
                missing[name] = cnt - current_cnt

        return missing

    def set_to_interactive(self) -> str:
        """Sets the mode to interactive"""
        self._mode = Mode.INTERACTIVE
        return "Interactive mode entered!"

    # Getters
    @property
    def inventory(self) -> dict[str, int]:
        return self._inventory.items

    @property
    def quests(self) -> dict[str, Quest]:
        return self._quests.copy()

    @property
    def mode(self) -> Mode:
        return self._mode
