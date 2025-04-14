# David Knowles
# 4/11/2025
# stores parent class for game objects
# stores classes for enemies and items 

from enemy_actions import ENEMY_ACTIONS_DICT as EAD
from random import randint
# used for returning an object by value instead of by reference 
import copy

EMPTY = "N/A"

# returns whatever type `key_` is paired with
# `key_` will usually be a string in my case, but its usage depends on the dictionary input
# used to safely assign values
def safe_assign(dictionary_input:dict, key_):
    try:
        rtrn_val = dictionary_input[key_]

        return rtrn_val
    except:
        return EMPTY


# parent class
class Game_Object:
    """
    `name` -> object name
    `description` -> object description
    `stats` -> stores object stats
    """
    def __init__(self, name:str = EMPTY, description:str = EMPTY):
        self.name = name
        self.description = description

        # empty dictionary
        self.stats = {}

    # adds a value to the `stats` dict
    def add_stat(self, key, value) -> None:
        self.stats[key] = value

    # useful for testing 
    def stats_str(self) -> str:
        stats_str = ""
        for key in self.stats:
            stats_str += f"{key}: {self.stats[key]}\n"

        return stats_str[:-1]

    def __str__(self) -> str:
        # Returns:
        """
        Name
        Description
        """
        return f"{self.name}\n{self.description}"

    def get_stats(self) -> dict:
        return self.stats

    def get_name(self) -> str:
        # originally had this written as `return self.Name`
        # oops!!!!
        return self.name

    def get_description(self) -> str:
        return self.description

# enemy class
class Enemy(Game_Object):

    # `self.attacks` stores the list of attacks the enemy can use

    def __init__(self, enemy_dict:dict):
        Game_Object.__init__(self, safe_assign(enemy_dict, "Name"), safe_assign(enemy_dict, "Description"))

        attacks_temp = safe_assign(enemy_dict, "Attacks").split(",")

        self.attacks = []

        for a in attacks_temp:
            self.attacks.append(safe_assign(EAD, a))

        # sets up the dictionary of stats
        # don't need to use safe assign here since we know that the key is in the dictionary
        for key in enemy_dict:
            if not key in {"Name", "Description", "Attacks"}:
                Game_Object.add_stat(self, key, enemy_dict[key])


    def __str__(self) -> str:
        return Game_Object.__str__(self) + "\nStats:\n" + Game_Object.stats_str(self)

    # picks a random attack from the enemy's attack list 
    def attack(self):
        element_id = randint(0, len(self.attacks) - 1)

        return self.attacks[element_id]


class Item(Game_Object):

    # dictionary that pairs item names to their object definition
    # used to initialize players (and enemies maybe?) with specific items in their inventory 
    item_dict = {}

    # function called to update item dictionary
    # `item_object` should be an Item 
    def update_item_dict(item_object):
        key = item_object.get_name().lower()

        Item.item_dict[key] = item_object
        print(key)

    # returns a copy of the item from the dictionary
    def get_item_from_dict(item_name:str):
        item_name = item_name.lower()

        return copy.deepcopy(Item.item_dict[item_name])


    def __init__(self, item_dict:dict):
        Game_Object.__init__(self, safe_assign(item_dict, "Name"), safe_assign(item_dict, "Description"))

        self.item_type = safe_assign(item_dict, "Type")

        # set up item stats
        for key in item_dict:
            if not key in {"Name", "Description", "Type"}:
                Game_Object.add_stat(self, key, item_dict[key])

        self.player_owned = False
        self.is_treasure = False

    # used to denote whether or not the item is contained within the player's inventory 
    def set_player_ownership(player_owns:bool) -> None:
        self.player_owned = player_owns

    # used to denote whether item is contained within a treasure chest
    # mainly used to know when price should be printed, since price shouldn't be printed if the item is free
    def set_is_treasure(is_treasure:bool) -> None:
        self.is_treasure = is_treasure

    def __str__(self) -> str:
        output_str = Game_Object.__str__(self)

        # adds object price if not in player inventory
        # this bool expression is kinda gross and icky but whatever 
        if not self.player_owned and "Price" in self.stats and not self.is_treasure:
            output_str += f"\n${self.stats["Price"]}"

        return output_str