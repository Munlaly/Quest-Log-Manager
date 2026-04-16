import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from QuestLogSystem.QuestLogManager import QuestLogManager, Mode
from QuestLogSystem.Quest import Quest


@pytest.fixture
def mock_manager(monkeypatch) -> QuestLogManager:
    """
    Creates a mock QuestLogManager with pre-loaded fake data.
    """

    fake_inventory = {"gold": 10, "potion": 2}
    fake_quests = {
        "buy sword": Quest(
            "Buy Sword", {"gold": 15}
        ),  # Not completable (Needs 15, we have 10)
        "heal up": Quest("Heal Up", {"potion": 1}),  # Completable!
        "epic boss": Quest(
            "Epic Boss", {"dragon scale": 1}
        ),  # Not completable (Missing item entirely)
    }

    monkeypatch.setattr(QuestLogManager, "load_inventory", lambda path: fake_inventory)
    monkeypatch.setattr(QuestLogManager, "load_quests", lambda path: fake_quests)

    monkeypatch.setattr(QuestLogManager, "save_inventory", lambda self: None)

    dummy_config = {
        "quest_file": "dummy.json",
        "inventory_file": "dummy.json",
        "reports_dir": "dummy",
        "processes_dir": "dummy",
    }

    return QuestLogManager(dummy_config)


# --- TESTS ---


def test_plan_filters_completable_quests(mock_manager):
    """Tests if plan correctly finds the completable quests"""
    # ACT
    completable_quests = mock_manager.plan()

    # ASSERT
    assert (
        len(completable_quests) == 1
    ), "Only one quest should be completable based on our mock data"
    assert (
        "Heal Up" in completable_quests
    ), "The 'Heal Up' quest should be identified as completable"


def test_gap_analysis_calculates_missing_amounts(mock_manager):
    """Tets if gap correctly finds the missing amount for items from the inventory"""
    # ACT
    missing = mock_manager.gap("buy sword")

    # ASSERT
    assert "gold" in missing, "Gap analysis should identify 'gold' is missing"
    assert missing["gold"] == 5, "We have 10 gold but need 15, gap should be exactly 5"


def test_gap_analysis_identifies_completely_missing_items(mock_manager):
    """Tests if gap correctly finds the missing amount for the items nt in the inventory"""
    # ACT
    missing = mock_manager.gap("epic boss")

    # ASSERT
    assert "dragon scale" in missing, "Items not in inventory at all must be tracked"
    assert missing["dragon scale"] == 1, "Gap should be the full requirement amount"


def test_gap_analysis_invalid_quest_raises_error(mock_manager):
    """Tests if gap called for invalid quest coorectly raises the expected error"""
    # ACT & ASSERT
    with pytest.raises(ValueError) as error_info:
        mock_manager.gap("nonexistent quest")

    assert "does not exist" in str(
        error_info.value
    ), "Must provide a clear error for invalid quests"


def test_complete_quest_success_consumes_items(mock_manager):
    """Tests if complete quest correctly consumes the items"""
    # ARRANGE
    initial_potions = mock_manager.inventory.get("potion")

    # ACT
    success_message = mock_manager.complete_quest("heal up")

    # ASSERT
    assert (
        mock_manager.inventory.get("potion") == initial_potions - 1
    ), "Completing the quest must consume the required items"
    assert (
        "successfully completed" in success_message
    ), "Must return the success string for the CLI to print"


def test_complete_quest_uncompletable_raises_error(mock_manager):
    """tests if complete quest called for uncompletable quest correctly raises expected error"""
    # ACT & ASSERT
    with pytest.raises(ValueError) as error_info:
        mock_manager.complete_quest("buy sword")

    assert "not completable" in str(
        error_info.value
    ), "System must actively block users from completing quests they don't have items for"


def test_set_to_interactive_changes_mode(mock_manager):
    """Tsets if mode can be changed to interactive"""
    # ARRANGE
    assert mock_manager.mode == Mode.DEFAULT, "Manager should boot in DEFAULT mode"

    # ACT
    mock_manager.set_to_interactive()

    # ASSERT
    assert (
        mock_manager.mode == Mode.INTERACTIVE
    ), "Mode must successfully update to INTERACTIVE"
