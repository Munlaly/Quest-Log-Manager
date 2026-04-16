import sys, os
import pytest

# setup path for project folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from QuestLogSystem.Inventory import Inventory


def test_inventory_use_item_decreases_stock():
    """Testing that using an item correctly reduces its quantity in the inventory."""

    # Arrange
    inv = Inventory({"potion": 10})
    initial_potions = inv.get_item_count("potion")

    # Act
    inv.use_item("potion", 5)

    # Assert
    assert (
        inv.get_item_count("potion") == initial_potions - 5
    ), "Inventory should decrease by the exact used amount (Criteria 13)"


def test_inventory_prevents_negative_usage():
    """Testing that the inventory blocks users from using negative quantities."""

    # Arrange
    inv = Inventory({"potion": 10})

    # Act & Assert
    with pytest.raises(ValueError) as error_info:
        inv.use_item("potion", -5)

    assert "Cannot remove a negative quantity" in str(
        error_info.value
    ), "The system must throw a specific error preventing negative usage."
