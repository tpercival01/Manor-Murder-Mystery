from typing import Dict, List, Tuple
import json

class GameState:
    def __init__(self) -> None:
        self.is_over: bool = False
        self.current_location: str = "garden"
        self.inventory: List[str] = []
        self.visited_locations: List[str] = []
        self.locations: Dict[str, Dict] = {
            "garden": {
                "description": (
                    "You stand at the edge of a manicured garden. The distant laughter and clinking "
                    "glasses of the evening’s party have gone eerily quiet since the discovery "
                    "of the body inside. The scent of roses and freshly cut grass mingles with the "
                    "smoke of your half-finished cigarette. Stone statues and hedges watch in silence. "
                    "The manor’s grand foyer lies to the east, its doors thrown open in panic."
                ),
                "exits": {"east": "foyer"},
                "items": ["cigarette_case", "matches"],
                "locked": False,
                "required_item": None
            },
            "foyer": {
                "description": (
                    "You step into the grand foyer where voices once rang out with laughter. Now, "
                    "the air feels heavy. Guests cluster in quiet groups, their eyes wide with shock. "
                    "On the marble floor, the host’s cousin lies lifeless, a bloody handkerchief "
                    "nearby. A sweeping staircase rises to the north. Doors lead off in multiple "
                    "directions: west to the drawing room, east to the study, and south to the kitchen."
                ),
                "exits": {
                    "west": "drawing_room",
                    "east": "study",
                    "south": "kitchen",
                    "north": "staircase"
                },
                "items": ["bloody_handkerchief"],
                "locked": False,
                "required_item": None
            },
            "drawing_room": {
                "description": (
                    "Plush armchairs and a velvet sofa frame a low table scattered with half-empty "
                    "glasses. A large family portrait looms over the mantelpiece, the subjects’ eyes "
                    "seeming to follow your every move. A locked window offers a view of the garden. "
                    "On a small side table, a letter with a broken wax seal begs for inspection."
                ),
                "exits": {"east": "foyer"},
                "items": ["mysterious_letter"],
                "locked": False,
                "required_item": None
            },
            "study": {
                "description": (
                    "A dimly lit study with an imposing mahogany desk and shelves packed with old "
                    "volumes. A pipe still smolders in an ashtray. The scent of old ink and leather "
                    "fills the air. A heavy velvet curtain hangs on the north wall, strangely out of "
                    "place. To the west, you can return to the foyer."
                ),
                "exits": {"west": "foyer", "north": "secret_library"},
                "items": ["old_key"],
                "locked": False,
                "required_item": None
            },
            "secret_library": {
                "description": (
                    "Pushing aside the velvet curtain, you enter a secret library, hidden behind the "
                    "study’s walls. Dusty shelves sag under the weight of ancient tomes and grim "
                    "treatises on poisons and scandal. A single candle burns on a desk holding an "
                    "incriminating ledger. This place feels like a shrine to secrets. From here, you "
                    "may only return south to the study."
                ),
                "exits": {"south": "study"},
                "items": ["incriminating_ledger"],
                "locked": True,
                "required_item": "lantern"   # It's too dark to safely navigate without a proper light source
            },
            "kitchen": {
                "description": (
                    "The kitchen’s warmth and savory aromas linger, though the servants are on edge. "
                    "Copper pots reflect the lamplight. A large butcher’s block sits in the center, "
                    "a carving knife embedded deep in its surface. Nervous whispers point to the cellar "
                    "door to the south, which is firmly locked. The garden lies to the west, and you "
                    "can return north to the foyer."
                ),
                "exits": {"north": "foyer", "west": "garden", "south": "cellar"},
                "items": ["carving_knife"],
                "locked": False,
                "required_item": None
            },
            "staircase": {
                "description": (
                    "The grand staircase ascends gracefully. As you climb, a hush falls. The murderer "
                    "could be lurking above. At the landing, you see a door to the guest bedroom to the "
                    "east, and a locked door to the west—surely the master bedroom. Portraits of the "
                    "family line the walls, their painted eyes filled with secrets."
                ),
                "exits": {"down": "foyer", "east": "guest_bedroom", "west": "master_bedroom"},
                "items": [],
                "locked": False,
                "required_item": None
            },
            "guest_bedroom": {
                "description": (
                    "A neat guest bedroom, prepared with care for visitors. The bed is made, the desk "
                    "beneath the window is orderly, and a perfume bottle sits on the vanity. The drapes "
                    "billow softly, and the open window leads onto a narrow balcony to the south. "
                    "If there were footsteps, they’ve been expertly erased."
                ),
                "exits": {"west": "staircase", "south": "balcony"},
                "items": ["perfume_bottle"],
                "locked": False,
                "required_item": None
            },
            "master_bedroom": {
                "description": (
                    "Before you is a heavily carved door—the master bedroom, no doubt. It's locked. "
                    "Rumors swirl about what could be inside: financial ledgers, private letters, "
                    "family disputes. If only you had the right key, you could uncover what the host "
                    "might be hiding here."
                ),
                "exits": {"east": "staircase"},
                "items": [],
                "locked": True,
                "required_item": "old_key"
            },
            "balcony": {
                "description": (
                    "Stepping onto the balcony, a gentle breeze ruffles your hair. Below, the dark "
                    "garden stretches out, hedges shaping shadows on the lawn. Guests still murmur "
                    "near the foyer doors, oblivious to you overhead. If you had something to help "
                    "you climb down quietly, you might reach a part of the grounds otherwise "
                    "unexplored. You can return north to the guest bedroom."
                ),
                "exits": {"north": "guest_bedroom", "down": "orchard"},
                "items": ["silk_scarf"],
                "locked": False,
                "required_item": None
            },
            "cellar": {
                "description": (
                    "A dank, dark cellar that smells of mold and old wine. Rows of dusty bottles "
                    "line the walls. Your footsteps echo ominously. In the corner stands a locked "
                    "metal grate. You sense passages or tunnels may lead elsewhere. Without proper "
                    "light, searching further seems risky."
                ),
                "exits": {"north": "kitchen"},
                "items": ["lantern"],
                "locked": True,
                "required_item": "carving_knife"  # Pry the cellar door or grate open with a sturdy blade
            },
            "orchard": {
                "description": (
                    "You descend into the orchard, a hidden grove of apple trees behind the manor. "
                    "Moonlight filters through the leaves, illuminating fallen fruit and the faint "
                    "outline of distant structures. To the east, you see a glassy silhouette of a "
                    "greenhouse dome, and to the south, a stable’s roof peeks over a hedge. The air "
                    "is cool, and the silence here is profound, as if nature itself holds its breath."
                ),
                "exits": {"north": "balcony", "east": "greenhouse", "south": "stable"},
                "items": ["orchard_ladder"],
                "locked": True,
                "required_item": "silk_scarf"   # Use the scarf from the balcony to safely climb down
            },
            "greenhouse": {
                "description": (
                    "A delicate structure of glass and iron, the greenhouse is packed with lush greenery "
                    "and exotic blooms. Condensation beads on the glass panes. A workbench at the back "
                    "holds gardening tools that might have been used to hide evidence. The orchard "
                    "lies to the west, a reminder of the quiet darkness outside."
                ),
                "exits": {"west": "orchard"},
                "items": ["pruning_shears"],
                "locked": True,
                "required_item": "old_key"   # The greenhouse door is locked. The old key might fit.
            },
            "stable": {
                "description": (
                    "Within the stable, horses shift nervously in their stalls. The scent of hay and "
                    "leather is strong. A rack of tools and bridles lines one wall, and a ladder leads "
                    "to a hayloft above. To the east, a narrow door leads to a small caretaker’s shack. "
                    "Tracks in the straw hint that someone passed through recently, possibly in haste."
                ),
                "exits": {"north": "orchard", "east": "caretaker_shack", "up": "hayloft"},
                "items": ["rope"],
                "locked": False,
                "required_item": None
            },
            "hayloft": {
                "description": (
                    "Climbing into the hayloft, you are surrounded by bales of dried grasses and a few "
                    "old tools. Dust motes dance in the sliver of moonlight coming through a cracked "
                    "board. It’s quiet here, perhaps too quiet, and you can see the stable floor below. "
                    "You can climb back down, but there may be something hidden among the hay."
                ),
                "exits": {"down": "stable"},
                "items": ["strange_token"],
                "locked": False,
                "required_item": None
            },
            "caretaker_shack": {
                "description": (
                    "The caretaker’s shack is a cramped space filled with old tools, racks of seed "
                    "packets, and dusty bottles. An oil lamp flickers on a rough-hewn table. A "
                    "carefully kept journal sits beside it. In the floorboards, you notice a trapdoor "
                    "leading down. Rumor has it these old estates often have secret escape routes. "
                    "To the west lies the stable."
                ),
                "exits": {"west": "stable", "down": "secret_tunnel"},
                "items": ["caretaker_journal"],
                "locked": False,
                "required_item": None
            },
            "secret_tunnel": {
                "description": (
                    "A narrow earthen tunnel runs beneath the estate. Moisture drips from the "
                    "ceiling, and your footsteps echo strangely. It’s utterly dark, save for the faint "
                    "glow of your lantern if you’ve brought it. Perhaps this leads back to the "
                    "cellar, or to another secret somewhere in the manor’s foundations."
                ),
                "exits": {"up": "caretaker_shack", "north": "cellar"},
                "items": [],
                "locked": True,
                "required_item": "lantern"   # Too dark to move safely without proper light
            }
        }

    def describe_current_location(self) -> str:
        loc = self.locations[self.current_location]
        desc = loc["description"]

        if loc["items"]:
            desc += "\n\nYou see: " + ", ".join(loc["items"])
        
        if self.current_location not in self.visited_locations:
            self.visited_locations.append(self.current_location)
        
        return desc
    
    def move_player(self, direction: str) -> Tuple[bool, str]:
        current_loc_data = self.locations[self.current_location]

        if direction in current_loc_data["exits"]:
            new_location = current_loc_data["exits"][direction]
            # Check if the new location is locked and if the player has required item
            if self.locations[new_location]["locked"]:
                required = self.locations[new_location]["required_item"]
                if required and required in self.inventory:
                    # Player can unlock the location
                    self.locations[new_location]["locked"] = False
                    return self._change_location(new_location, f"You unlock the path and move {direction}.")
                else:
                    return False, f"The path to the {new_location} is locked. You need {required} to proceed."
            else:
                # The location is not locked
                return self._change_location(new_location, f"You move {direction}.")
        else:
            return False, "You can't go that way."

    def _change_location(self, new_location: str, success_message: str) -> Tuple[bool, str]:
        self.current_location = new_location
        return True, success_message

    def pick_up_item(self, item_name: str) -> Tuple[bool, str]:
        loc_data = self.locations[self.current_location]
        if item_name in loc_data["items"]:
            loc_data["items"].remove(item_name)
            self.inventory.append(item_name)
            return True, f"\nYou pick up the {item_name}."
        else:
            return False, f"\nThere is no {item_name} here."

    def use_item(self, item_name: str) -> Tuple[bool, str]:
        if item_name not in self.inventory:
            return False, f"You don't have a {item_name}."

        current_loc = self.current_location
        loc_data = self.locations[current_loc]

        # 1. Old Key - Unlock locations
        if item_name == "old_key":
            if current_loc == "master_bedroom":
                return True, "You turn the old key in the heavy lock. The master bedroom is now accessible."
            elif current_loc == "greenhouse":
                return True, "The old key turns smoothly, and the greenhouse door clicks open."
            else:
                return False, "You try the old key, but find nothing here to unlock."

        # 2. Carving Knife - Pry open cellar from the kitchen if locked
        if item_name == "carving_knife":
            if current_loc == "kitchen" and "cellar" in loc_data["exits"] and self.locations["cellar"]["locked"]:
                self.locations["cellar"]["locked"] = False
                return True, "You wedge the carving knife into the cellar door’s seam and pry it open."
            else:
                return False, "You brandish the carving knife, but there's nothing here to force open."

        # 3. Lantern - Use in dark places to reveal surroundings
        if item_name == "lantern":
            # Check if location is dark and requires light
            if current_loc in ("secret_library", "secret_tunnel"):
                return True, "You raise the lantern, and its warm glow illuminates hidden details in the darkness."
            else:
                return False, "You hold up the lantern, but there's already enough light here."

        # 4. Silk Scarf - Justify descending from balcony to orchard
        if item_name == "silk_scarf":
            if current_loc == "balcony" and "down" in loc_data["exits"]:
                # Maybe ensure orchard was locked and now is safely accessible
                return True, "You secure the silk scarf and use it to safely descend below."
            else:
                return False, "You hold the silk scarf in your hands. Soft, but not particularly useful here."

        # 5. Pruning Shears - Reveal something hidden in greenhouse
        if item_name == "pruning_shears":
            if current_loc == "greenhouse":
                # Reveal a hidden item
                self.locations["greenhouse"]["items"].append("rare_seed_pouch")
                return True, "You snip away some overgrown vines, revealing a small pouch of rare seeds!"
            else:
                return False, "You open and close the pruning shears futilely. Nothing to cut here."

        # 6. Rope - Secure rope in stable or orchard for flavor
        if item_name == "rope":
            if current_loc == "stable":
                return True, "You tie the rope securely to a beam, making it easier to move around the stable."
            elif current_loc == "orchard":
                return True, "You tie the rope around a sturdy branch, feeling more secure in your footing."
            else:
                return False, "You hold the rope, but there's nowhere obvious to secure it."

        # 7. Caretaker Journal - Provide clues in caretaker_shack
        if item_name == "caretaker_journal":
            if current_loc == "caretaker_shack":
                return True, "You flip through the journal by lantern light. The caretaker noted someone slipping into the secret tunnel late at night."
            else:
                return False, "You glance at the journal, but this doesn't seem like the right place to learn more."

        # 8. Matches - Light the lantern in dark areas if you have one
        if item_name == "matches":
            if "lantern" in self.inventory and current_loc in ("secret_library", "secret_tunnel"):
                return True, "You strike a match and light the lantern. The darkness recedes."
            else:
                return False, "You strike a match. It flares briefly before dying out, accomplishing little here."

        # 9. Incriminating Ledger - End game in master_bedroom if you have correct evidence
        if item_name == "incriminating_ledger":
            if current_loc == "master_bedroom":
                # Check if you have old_key and ledger to confront the murderer
                if "old_key" in self.inventory and "incriminating_ledger" in self.inventory:
                    self.is_over = True
                    return (True, 
                            "\nYou open the incriminating ledger before the host, revealing every debt and "
                            "secret. The host pales as you declare: 'You are the murderer.' Gasps fill the air "
                            "as the truth comes crashing down.\n\nThe mystery is solved, and the game ends.")
                else:
                    return False, "\nYou show the ledger, but something is missing. You need all crucial evidence to accuse the murderer."

        # 10. Mysterious Letter - Maybe reveal extra hints in the drawing room
        if item_name == "mysterious_letter":
            if current_loc == "drawing_room":
                return True, "You re-read the letter here, comparing its handwriting to the portrait’s figures. It intensifies your suspicion of the family’s secrets."
            else:
                return False, "You unfold the letter, but learn nothing new in this location."

        # Items with no special use, just a generic message
        if item_name in ("cigarette_case", "bloody_handkerchief", "strange_token", "perfume_bottle", "orchard_ladder"):
            return False, f"You examine the {item_name}, but it doesn't seem to have any special use here."

        # Default response if no condition matches
        return False, "You can't use that here."



    def examine_item(self, item_name: str) -> str:
        known_items = {
            "cigarette_case": (
                "A silver case with elegant initials that match the host’s surname. "
                "Inside, only faint tobacco residue remains. Its owner might have stepped away in a hurry."
            ),
            "matches": (
                "A small box of matches with the manor’s crest printed on it. "
                "These could ignite your lantern or rekindle a clue hidden in the darkness."
            ),
            "bloody_handkerchief": (
                "A once-fine handkerchief, now stained deep red. The embroidery on the corner "
                "looks like it could match the victim’s monogram. A silent witness to the crime."
            ),
            "mysterious_letter": (
                "A letter with a broken seal and frantic handwriting. It warns of hidden debts, "
                "whispers of blackmail, and dire consequences if secrets are not revealed."
            ),
            "old_key": (
                "An old iron key with intricate detailing. It seems important—perhaps it opens a "
                "heavily locked door to a place where only the owner dared to tread."
            ),
            "incriminating_ledger": (
                "A heavy ledger filled with records of illicit dealings, unpaid debts, and names "
                "that should never see the light of day. This is the heart of a deadly motive."
            ),
            "carving_knife": (
                "A sturdy kitchen knife, its blade still sharp enough to pry open more than just a lock. "
                "In the right (or wrong) hands, it could have ended a life."
            ),
            "lantern": (
                "A wrought-iron lantern with a sooty glass pane. If lit, it will illuminate the darkest halls, "
                "revealing hidden rooms and long-buried secrets."
            ),
            "silk_scarf": (
                "A fine silk scarf, strong yet delicate. With it, you could descend from a height safely—"
                "or perhaps retrace someone’s clandestine escape route."
            ),
            "orchard_ladder": (
                "A folding ladder stashed outdoors. Perfect for reaching high places or safely navigating "
                "treacherous terrain. Whoever used it likely knew these grounds well."
            ),
            "pruning_shears": (
                "Heavy-duty gardening shears. With them, overgrown foliage could be cleared, "
                "uncovering concealed evidence or a secret path."
            ),
            "rope": (
                "A length of sturdy rope, suitable for climbing or securing loads. "
                "A resourceful visitor might use it to access areas otherwise unreachable."
            ),
            "strange_token": (
                "A small, carved token bearing foreign symbols. Its origin is unclear, but it may link "
                "to old debts or distant transactions hinted at in the ledger."
            ),
            "caretaker_journal": (
                "A meticulously kept journal detailing arrivals, departures, and late-night movements. "
                "Its observations could place someone at the scene of the crime at the wrong time."
            ),
            "perfume_bottle": (
                "A delicate glass bottle with a faint floral scent. A personal touch that might connect "
                "a guest—or the victim—to a particular room or secret rendezvous."
            )
        }


        if item_name in self.inventory or item_name in self.locations[self.current_location].get("items", []):
            return known_items.get(item_name, f"It's a {item_name}. Nothing special.")
        else:
            return f"You don't see a {item_name} here, and you don't have it in your inventory."

    def save_state(self) -> Dict:
        return {
            "current_location": self.current_location,
            "inventory": self.inventory,
            "visited_locations": self.visited_locations
        }
    
    def save_to_file(self, filename:str) -> None:
        state = self.save_state()
        with open(filename, "w") as f:
            json.dump(state,f,indent=4)

    def load_state(self, state: Dict) -> None:
        self.current_location = state.get("current_location", "starting_room")
        self.inventory = state.get("inventory", [])
        self.visited_locations = state.get("visited_locations", [])
    
    def load_from_file(self, filename: str) -> None:
        with open(filename, "r") as f:
            state = json.load(f)
            self.load_state(state)