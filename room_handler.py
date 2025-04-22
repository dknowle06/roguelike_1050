"""
4/22/2025
David Knowles

File that handles room actions
"""

from mapgeneration import *
from player import Player 

from common_funcs import *


# exception raised when user's input is invalid
class BadInputException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        return f"{self.msg}"


# function used to handle input, called by `room_handler`
# returns a boolean value to let the program know if the turn is over, in the event of being in a battle
# player should be a player object 
def input_handler(user_input:str, elements:list, player) -> bool:
    # parses user input into a list
    # first element should be the command
    # second element should be the command parameter 
    parsed_input = user_input.upper().split()

    if len(parsed_input) < 2 and parsed_input[0] not in {"INVENTORY", "NEXT", "CONTINUE"}:
        raise BadInputException(VALID_ACTION)

    command = parsed_input[0]

    try:
        parameter = int(parsed_input[1]) if len(parsed_input) > 1 else 0
    except:
        raise BadInputException(VALID_ACTION)

    # check allows the player to view enemey stats, doesn't progress the battle
    if command == "CHECK":
        if parameter not in range(1, len(elements) + 1):
            raise BadInputException(VALID_ACTION)

        print(f"\n{elements[parameter - 1]}\n")

        return False

    # inventory allows the player to view their inventory, doesn't progress the battle
    elif command == "INVENTORY":
        print(f"\n{player.inventory_as_str()}\n")

        return False

    elif command == "EQUIP":
        if parameter not in range(1, len(player.inventory) + 1):
            raise BadInputException(VALID_ACTION)
        elif player.inventory[parameter - 1].item_type.upper() != "WEAPON":
            raise BadInputException("Can only equip weapons!")

        player.set_equipped_weapon(parameter - 1)

        print(f"\nYou equipped your {player.inventory[parameter - 1].get_name()}!\n")

        return True



# room should be a room object 
# player should be a player object
def room_handler(room, player):
    room_id = room.get_id()

    room_loop = True

    # `range(0,3)` includes the ids for enemy encounter, miniboss encounter, and boss encounter 
    if room_id in range(0,3):
        print(f"You enter a room, and get ambushed by some enemies!\n")

        enemies = room.get_encounter().get_elements()
        enemy_names = [x.get_name() for x in enemies]

        while room_loop:
            print(list_to_string(enemy_names))
            print("What do you want to do?")

            gathering_input = True

            enemy_turn = False

            while gathering_input:
                user_action = input_validation("", VALID_ACTION, lambda a: a.split()[0] in ATTACK_COMMS)

                # if an exception isn't raised, we know the player's input is done! 
                try:
                    enemy_turn = input_handler(user_action, enemies, player)

                    gathering_input = False
                except BadInputException as e:
                    enemy_turn = False
                    print(e, end="")

            if enemy_turn:
                print("ENEMY TURN PLACEHOLDER")

                