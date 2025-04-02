# stores parent class for game objects
# stores classes for enemies and items 

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

# enemy class
class Enemy(Game_Object):

    # `self.attacks` stores the list of attacks the enemy can use

    def __init__(self, enemy_dict:dict):
        Game_Object.__init__(self, safe_assign(enemy_dict, "Name"), safe_assign(enemy_dict, "Description"))

        attacks_temp = safe_assign(enemy_dict, "Attacks").split(",")
        # TODO: add a function that assigns `self.attacks` to a list of attack functions

        self.attacks = []

        # sets up the dictionary of stats
        # don't need to use safe assign here since we know that the key is in the dictionary
        for key in enemy_dict:
            if not key in {"Name", "Description", "Attacks"}:
                Game_Object.add_stat(self, key, enemy_dict[key])


    def __str__(self) -> str:
        return Game_Object.__str__(self) + "\nStats:\n" + Game_Object.stats_str(self)


class Item(Game_Object):

    def __init__(self, item_dict:dict):
        Game_Object.__init__(self, safe_assign(item_dict, "Name"), safe_assign(item_dict, "Description"))

        # `stats` is going to be much more railroaded for items than enemies, since i will use functions to augment player stats with items

        Game_Object.add_stat(self, "Price", safe_assign(item_dict, "Price"))

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