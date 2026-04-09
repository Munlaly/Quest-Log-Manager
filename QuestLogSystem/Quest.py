class Quest:
    def __init__(self, name: str, items: dict[str, int] | None = None) -> None:
        self.name: str = name

        if items is None:
            self._items: dict[str, int] = {}
        else:
            self._items: dict[str, int] = items.copy()

    def __str__(self) -> str:
        output: list[str] = [f"Quest: {self.name}"]

        if self.items:
            output.append("Required Items:")
            for name, quantity in self.items.items():
                output.append(f"\t-{name}: {quantity}")
        else:
            output.append("Required Items: None")

        return "\n".join(output)

    def __repr__(self) -> str:

        return f"name= {self.name!r}, items= {self.items!r}"

    @property
    def items(self) -> dict[str, int]:
        """Returns a safe, read-only copy of the quest requirements."""
        return self._items.copy()
