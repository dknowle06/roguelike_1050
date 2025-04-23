"""
David Knowles 
4/23/2025
Class containing player information
"""

from dict_parser import dict_parser
from game_object import Item
from common_funcs import list_to_string

class Player:
    # set of all possible player actions
    # irrelevant set, i'm gonna keep it just in case but for now it's gonna stay commented out 
    # PLAYER_ACTIONS = {"CHECK", "ATTACK", "EQUIP", "TOSS", "BUY", "SELL"}

    def __init__(self, name:str, stats_filepath:str = "dictionaries/player_stats.txt"):
        self.name = name
        self.stats = {}

        self.level = 1
        self.exp_total = 0

        # i have to use `[0]` here, since `dict_parser` returns a list of dictionaries ...
        # ... and i want to access the first and (ideally) only item in the list
        stats_temp = dict_parser(stats_filepath, ":", True)[0]

        # assigns the player's inventory
        # crashes if it's undefined, and gives an error message
        try:
            inventory_temp = stats_temp["Starting Inventory"].split(",")
            del stats_temp["Starting Inventory"]

            self.inventory = [Item.item_dict[x] for x in inventory_temp]

            for i in self.inventory:
                i.set_player_ownership(True)
                
        except KeyError as e:
            print(f"{e}\n\"starting_inventory\" undefined in {stats_filepath} or items not properly initialized.")
            quit()

        self.equipped_weapon = None

        self.stats = stats_temp

        # used to store status effects
        self.stat_fx = {}

    def get_stats(self) -> dict:
        return self.stats

    def get_stat(self, key:str):
        return self.stats[key]

    # sets the player's equipped weapon
    # has no checks to ensure the player is equipping a weapon, that is something that the input handler should do 
    def set_equipped_weapon(self, idx:int):
        self.equipped_weapon = self.inventory[idx]

    def __str__(self) -> str:
        return f"You are {self.name}.\nYou are level {self.level} and have {self.exp_total} experience points.\nYou currently have a(n) {self.equipped_weapon.get_name()} equipped."

    # converts the inventory array into a string that looks prettier for printing 
    def inventory_as_str(self) -> str:
        output = []

        for i in self.inventory:
            output.append(i.get_name())

        return list_to_string(output)