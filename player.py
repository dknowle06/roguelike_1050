"""
David Knowles 
4/21/2025
Class containing player information
"""

from dict_parser import dict_parser
from game_object import Item

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
        except KeyError as e:
            print(f"{e}\n\"starting_inventory\" undefined in {stats_filepath} or items not properly initialized.")
            quit()


        self.stats = stats_temp

        # used to store status effects
        self.stat_fx = {}

    def get_stats(self) -> dict:
        return self.stats

    def __str__(self) -> str:
        return f"You are {self.name}.\nYou are level {self.level} and have {self.exp_total} experience points."