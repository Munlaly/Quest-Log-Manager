class Inventory:
    def __init__(self, items: dict[str, int] = None) -> None:
        if items is None:
            self.items = {}
        else:
            self.items = items.copy()

    def __str__(self) -> str:
        output: list[str] = ["Inventory:"]

        for item, cnt in self.items.items():
            output.append(f"\t{item} : {cnt}")

        return "\n".join(output)

    def __repr__(self) -> str:
        return f"items= {str(self.items)}"

    def add_item(self, name: str, cnt: int) -> None:
        """Adds a given number of an item to the inventory"""
        self.items[name] = self.items.get(name, 0) + cnt

    def use_item(self, name: str, cnt: int) -> None:
        """
        Removes a given number of an item from the inventory
        Throws error if the item doesn't exist in the inventory or if there is to few of it
        """

        num_item = self.items.get(name, 0)

        if not self.is_available(name, cnt):
            raise ValueError(f"Cannot use {cnt} {name}, because {num_item} exists!")
        else:
            self.items[name] -= cnt

    def is_available(self, name: str, cnt: int = 0) -> bool:
        """
        Checks if a given amount of an item is available
        If called with 2 arguments only checks if the item is in the dict
        """
        return self.items.get(name, 0) >= cnt
