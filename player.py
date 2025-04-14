"""
David Knowles 
4/11/2025
Class containing player information
"""

from dict_parser import dict_parser
from game_object import Item

class Player:
    def __init__(self, name:str, stats_filepath:str = "dictionaries/player_stats.txt"):
        self.name = name

        stats_temp = dict_parser(stats_filepath, ":", True)

        # assigns the player's inventory
        # crashes if it's undefined, and gives an error message
        try:
            inventory_temp = stats_temp["Starting Inventory"].split(",")
            del stats_temp["Starting Inventory"]

            self.inventory = [Item.item_dict[x] for x in inventory_temp]
        except KeyError as e:
            print(f"{e}\n\"starting_inventory\" undefined in {stats_filepath} or items not properly initialized.")
            quit()

        # used to store status effects
        self.temp_stats = {}

    def get_stats(self) -> dict:
        return self.stats