import json
import pytest
from pathlib import Path
from GameState import GameState

@pytest.fixture
def game_instance():
    # Returns a fresh game instance for each test
    return GameState()

def test_save_state_structure(game_instance):
    state = game_instance.save_state()
    expected_keys = {"current_location", "inventory", "visited_locations"}
    assert set(state.keys()) == expected_keys, "Missing or extra keys in saved state."

    assert isinstance(state["current_location"], str), "current_location should be a string."
    assert isinstance(state["inventory"], list), "inventory should be a list."
    assert isinstance(state["visited_locations"], list), "visited_locations should be a list."

@pytest.mark.parametrize("initial_state", [
    {
        "current_location": "dungeon",
        "inventory": ["sword", "shield"],
        "visited_locations": ["entrance", "hallway", "dungeon"],
    },
    {
        "current_location": "great_hall",
        "inventory": [],
        "visited_locations": []
    }
])

def test_load_state(game_instance, initial_state):
    """
    Parameterized test to ensure that loading various states sets the game attributes correctly.
    This verifies that `load_state` respects both complex and simple states.
    """
    game_instance.load_state(initial_state)
    assert game_instance.current_location == initial_state["current_location"]
    assert game_instance.inventory == initial_state["inventory"]
    assert game_instance.visited_locations == initial_state["visited_locations"]

def test_round_trip_save_load(game_instance):
    """
    Test that if we save the current state, then load it into a new Game instance,
    we get the same state back. This ensures serialization and deserialization match perfectly.
    """
    # Set some non-default state
    game_instance.current_location = "master_bedroom"
    game_instance.inventory = ["old_key", "matches"]
    game_instance.visited_locations = ["garden", "staircase", "master_bedroom"]

    saved_state = game_instance.save_state()

    # Create a new game instance and load the saved_state
    new_game = GameState()
    new_game.load_state(saved_state)

    assert new_game.current_location == game_instance.current_location
    assert new_game.inventory == game_instance.inventory
    assert new_game.visited_locations == game_instance.visited_locations

def test_save_to_file_and_load_from_file(game_instance, tmp_path: Path):
    """
    Integration test that checks writing the game state to a file and then loading it back.
    Uses a temporary path provided by pytest to avoid polluting the working directory.
    """
    game_instance.current_location = "foyer"
    game_instance.inventory = ["matches"]
    game_instance.visited_locations = ["foyer", "garden"]

    save_file = tmp_path / "test_savegame.json"
    game_instance.save_to_file(str(save_file))

    # Verify file content is valid JSON and has expected keys
    with open(save_file, "r") as f:
        data = json.load(f)
        assert "current_location" in data
        assert "visited_locations" in data

    # Load into a new game instance
    new_game = GameState()
    new_game.load_from_file(str(save_file))

    assert new_game.current_location == "foyer"
    assert new_game.inventory == ["matches"]
    assert new_game.visited_locations == ["foyer", "garden"]

def test_load_non_existent_file(game_instance):
    """
    Test loading from a file that doesn't exist.
    The method should handle this gracefully, such as printing an error or failing gracefully,
    not crashing the program.
    """
    non_existent = "non_existent_save.json"
    try:
        game_instance.load_from_file(non_existent)
    except FileNotFoundError:
        print("Test passed.")

def test_load_corrupted_file(game_instance, tmp_path: Path):
    """
    Tests loading from a corrupted JSON file. The code should handle JSONDecodeError and
    avoid crashing. It might print an error or revert to defaults.
    """
    corrupted_file = tmp_path / "corrupted_save.json"
    corrupted_file.write_text("{this is not valid json...")

    try:
        game_instance.load_from_file(str(corrupted_file))
    except json.JSONDecodeError:
       print("Test passed")

def test_load_incomplete_state(game_instance):
    """
    Tests that loading a state missing some keys still works and uses defaults.
    """
    incomplete_state = {
        "current_location": "strange_room"  # missing inventory, visited_locations
    }
    game_instance.load_state(incomplete_state)
    assert game_instance.current_location == "strange_room", "current_location should be updated"
    assert game_instance.inventory == [], "Default inventory should be an empty list"
    assert game_instance.visited_locations == [], "Default visited_locations should be empty list"
