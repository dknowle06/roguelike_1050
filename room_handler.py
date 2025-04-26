"""
4/26/2025
David Knowles

File that handles room actions
BadInputException is an exception raised when the input_handler function is fed bad input
input_handler chooses what to do based off what the player inputs 
room_handler handles calls to input_handler based off of the room type 

This file is, unfortunately, probably going to be the largest file for this program.
It would've been smart of me to split this into a couple different files, but it's too late for that now. 
"""

from mapgeneration import *
from player import Player 
import copy
from common_funcs import *


# exception raised when user's input is invalid
# there isn't much functionally different between this and the exception superclass 
# the main difference is a default parameter for the exception message
# `VALID_ACTION` is defined within `common_funcs.py`
class BadInputException(Exception):
    def __init__(self, msg:str = VALID_ACTION):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        return f"{self.msg}"


# NOTE: Sets used to check for validity of player commands found in `common_funcs.py`

# function used to handle input, called by `room_handler`
# returns a boolean value to let the program know if the turn is over, in the event of being in a battle
# player should be a player object 
def input_handler(user_input:str, elements:list, player, map_str:str) -> bool:
    # parses user input into a list
    # first element should be the command
    # second element should be the command parameter 
    parsed_input = user_input.upper().split()

    if len(parsed_input) < 2 and parsed_input[0] not in {"INVENTORY", "NEXT", "CONTINUE", "MAP", "SELF"}:
        raise BadInputException()

    command = parsed_input[0]
    parameter = None

    try:
        parameter = int(parsed_input[1]) if len(parsed_input) > 1 else 0
    except:
        raise BadInputException()

    # check allows the player to view enemey stats, doesn't progress the battle
    if command == "CHECK":
        if parameter not in range(1, len(elements) + 1):
            raise BadInputException()

        print(f"\n{elements[parameter - 1]}\n")

        return False

    # inventory allows the player to view their inventory, doesn't progress the battle
    elif command == "INVENTORY":
        print(f"\n{player.inventory_as_str()}\n")

        return False

    elif command == "EQUIP":
        if parameter not in range(1, len(player.inventory) + 1):
            raise BadInputException()
        # raises an exception if the player attempts to equip something that isn't a weapon
        elif player.inventory[parameter - 1].item_type.upper() != "WEAPON":
            raise BadInputException("Can only equip weapons!")

        player.set_equipped_weapon(parameter - 1)

        print(f"\nYou equipped your {player.inventory[parameter - 1].get_name()}!\n")

        return True

    elif command == "ATTACK":
        # raise exception if player attempts to attack and enemy that doesn't exist
        if parameter not in range(1, len(elements) + 1):
            raise BadInputException()

        # gather player stats
        player_attack = player.get_stat("Attack")
        player_sp_attack = player.get_stat("Special Attack")

        # create a reference to the enemy
        index = parameter - 1
        enemy = elements[index]

        # gather enemy stats
        enemy_defense = enemy.get_stat("Defense")
        enemy_sp_defense = enemy.get_stat("Special Defense")

        # gather weapon stats
        weapon_attack = player.equipped_weapon.get_stat("Attack")
        weapon_type = player.equipped_weapon.get_stat("Weapon Type")

        # calculate damage amount 
        damage = 0

        if weapon_type == "physical":
            damage = (weapon_attack + player_attack) / ((enemy_defense + 100) / 100)

        elif weapon_type == "special":
            damage = (weapon_attack + player_sp_attack) / ((enemy_sp_defense + 100) / 100)

        elif weapon_type == "piercing": # piercing damage only depends on the weapon stat 
            damage = weapon_attack

        newline()

        print(f"You dealt {damage:.1f} {weapon_type} damage to {enemy.get_name()} [{parameter}]!")

        # deal damage! 
        enemy.take_damage(damage)

        print(f"{enemy.get_name()} [{parameter}] now has {enemy.get_stat("Hp"):.1f} Hp.")

        # removes enemy from elements list if the enemy is defeated 
        if enemy.get_stat("Hp") <= 0:
            print(f"You defeated {enemy.get_name()} [{parameter}]!")

            elements.pop(index)

        newline()

        return True

    elif command == "MAP":
        print(f"\nDungeon map:\n{map_str}\n")

        return False
    
    elif command == "SELF":
        newline()
        print(player)
        newline()

    # commands that allow for navigating rooms!! 
    elif command in {"NEXT", "CONTINUE"}:
        if len(elements) == 1:
            print("\nYou continue on to the next room...\n")

            elements.append(1)

        elif len(elements) == 2:
            print("\nYou come across two doors, which one will you enter?\n\t[1] [2]")

            room_num = int(input_validation("", VALID_ACTION, lambda a: a.split()[0] in {"1", "2"}))
            room_ref = elements[room_num - 1]

            print(f"\nYou walk through the {"first" if room_num == 1 else "second"} door.\n")

            # turn the room list into a list that only contains the room the player chose 

            # empties the list while preserving the reference
            for i in range(2):
                elements.pop(0)

            elements.append(room_ref)

            # add an id shifter
            elements.append(1 if room_num == 1 else 3)

        elif len(elements) == 3:
            print("\nYou come across three doors, which one will you enter?\n\t[1] [2] [3]")

            room_num = int(input_validation("", VALID_ACTION, lambda a: a.split()[0] in {"1", "2", "3"}))
            room_ref = elements[room_num - 1]

            # nested ternary operator... ewwww
            print(f"\nYou walk through the {"first" if room_num == 1 else "second" if room_num == 2 else "third"} door.\n")

            # empties the list while preserving the reference
            for i in range(3):
                elements.pop(0)

            elements.append(room_ref)

            # add an id shifter
            elements.append(1 if room_num == 1 else 3 if room_num == 2 else 5)

        return True



# room should be a room object 
# player should be a player object
def room_handler(room, player, map_str:str):
    room_id = room.get_id()

    room_loop = True

    # `range(0,3)` includes the ids for enemy encounter, miniboss encounter, and boss encounter 
    if room_id in range(0,3):
        """
        ENEMIES
        MINIBOSSES
        BOSSES

        LOOK HERE FOR CODE DEFINING THESE ENCOUNTERS!!!!!!!!!!!!!!!!!!!!!
        """

        enemies = room.get_encounter().get_elements()
        enemy_names = ""

        # prints the miniboss or boss's name if this is a boss encounter
        # else, just print "some enemies"
        print(f"You enter a room, and get ambushed by {"some enemies" if room_id == ROOM_TYPES.FIGHT else f"the {enemies[0].get_name()}"}!\n")
        
        # used to determine gold and exp obtained at the end of an encounter 
        enemies_archive = copy.deepcopy(enemies)

        while room_loop:
            enemy_names = [x.get_name() for x in enemies]

            print(list_to_string(enemy_names))
            print("What do you want to do?")

            gathering_input = True

            enemy_turn = False

            while gathering_input:
                user_action = input_validation("", VALID_ACTION, lambda a: a.split()[0] in ATTACK_COMMS)

                # if an exception isn't raised, we know the player's input is done! 
                try:
                    enemy_turn = input_handler(user_action, enemies, player, map_str)

                    gathering_input = False
                except BadInputException as e:
                    enemy_turn = False
                    print(e, end="")

            if enemy_turn:
                print("ENEMY TURN PLACEHOLDER\n")

            # if all enemies have been defeated, end the room encounter 
            # add dropped gold and exp to player 
            if len(enemies) == 0:
                room_loop = False

                print("Congratulations! You have defeated all enemies in the room!")

                exp_dropped = 0
                gold_dropped = 0

                # sum up the total exp and gold 
                for enemy in enemies_archive:
                    exp_dropped += enemy.get_stat("Exp Dropped")
                    gold_dropped += enemy.get_stat("Gold Dropped")

                print(f"You found {gold_dropped} gold!")
                print(f"You gained {exp_dropped} experience points!")

                player.add_gold(gold_dropped)
                player.add_exp(exp_dropped)

                newline()
    
    # heals the player,
    # and then kicks them out!!
    elif room_id == ROOM_TYPES.FOUNTAIN:
        pass 