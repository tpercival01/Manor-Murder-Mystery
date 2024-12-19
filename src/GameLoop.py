import json

def run_game_loop(game_state):
    print("\nYou were invited as a guest to tonight’s grand soiree at the manor. You step into the garden,")
    print("lighting a cigarette under the moonlight. The scent of roses and freshly trimmed hedges soothes you,")
    print("when suddenly—a scream echoes from the foyer. The chatter and laughter that once filled the air fall silent,")
    print("replaced by the hushed murmurs of alarm. A body has been discovered.")
    print("\nAs an experienced detective, you flick your cigarette aside and steel yourself. It’s time to investigate.")
    print("\nType 'help' for a list of commands, and 'look' to examine your surroundings.")

    while not game_state.is_over:
        print("")
        user_command = input("> ")

        result = process_command(user_command, game_state)

        game_state.save_to_file("savegame.json")

        if result:
            print(result)

        if game_state.is_over:
            print("\nThanks for playing.")
            break

def process_command(user_command, game_state):
    cmd = user_command.strip().lower()

    # Quit the game
    if cmd in ("quit", "exit", "q"):
        game_state.is_over = True
        return "\nYou choose to step away, leaving the mystery unsolved."
    
    elif cmd.startswith("load"):
        try:
            game_state.load_from_file("savegame.json")
            print("Game successfully loaded!")
        except FileNotFoundError:
            print("No save game file found.")
        except json.JSONDecodeError:
            print("File is corrupted.")

    # Look around
    elif cmd.startswith("look"):
        # Describe the current location thoroughly
        location_name = game_state.current_location.replace("_", " ").title()

        return f"\nYou are currently in the {location_name}.\n\n{game_state.describe_current_location()}"

    # Move in a direction
    elif cmd.startswith("move"):
        parts = cmd.split()
        if len(parts) > 1:
            direction = parts[1]
            success, message = game_state.move_player(direction)
            if success:
                # After moving successfully, describe the new location
                location_description = game_state.describe_current_location()
                location_name = game_state.current_location.replace("_", " ").title()
                return f"\n{message}\n\nYou are now in the {location_name}.\n\n{location_description}"
            else:
                return message
        else:
            return "Move where? Try 'move north', 'move east', etc."

    # Take an item
    elif cmd.startswith("take"):
        parts = cmd.split(maxsplit=1)
        if len(parts) > 1:
            item_name = parts[1]
            success, message = game_state.pick_up_item(item_name)
            if success:
                # Mention the updated inventory after picking up an item
                inv = ", ".join(game_state.inventory) if game_state.inventory else "nothing"
                return f"{message}\n\nYou now carry: {inv}"
            else:
                return message
        else:
            return "Take what? Specify an item name."

    # Use an item
    elif cmd.startswith("use"):
        parts = cmd.split(maxsplit=1)
        if len(parts) > 1:
            item_name = parts[1]
            success, message = game_state.use_item(item_name)
            if success:
                # Using an item might change the environment or inventory
                inv = ", ".join(game_state.inventory) if game_state.inventory else "nothing"
                return f"{message}\nYour current inventory: {inv}"
            else:
                return message
        else:
            return "Use what? Specify an item you currently have."
    
    elif cmd.startswith("examine"):
        parts = cmd.split(maxsplit=1)
        if len(parts) > 1:
            item_name = parts[1]
            # Attempt to examine the specified item via the game_state method.
            message = game_state.examine_item(item_name)
            return message
        else:
            return "Examine what? Specify an item to examine."

    # Check inventory
    elif cmd in ("inventory", "inv"):
        inv = ", ".join(game_state.inventory) if game_state.inventory else "nothing"
        return f"\nYou currently carry: {inv}"

    # Help/Commands
    elif cmd in ("help", "commands"):
        return (
            "Available commands:\n"
            "  look              - Describe your current surroundings.\n"
            "  move <direction>  - Move north, south, east, west, etc.\n"
            "  take <item>       - Pick up an item in your current location.\n"
            "  use <item>        - Use an item from your inventory.\n"
            "  inventory (inv)   - Check what you are carrying.\n"
            "  quit              - Quit the game.\n"
            "\n"
            "Hints:\n"
            "  - 'look' often to rediscover details about your location.\n"
            "  - If you find keys or tools, 'use' them where appropriate.\n"
        )

    # Unrecognized commands
    else:
        return "You mutter something unintelligible. Try typing 'help' for a list of commands."

