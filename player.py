"""
David Knowles 
4/24/2025
Class containing player information
"""

from dict_parser import dict_parser
from game_object import Item
from common_funcs import list_to_string

EXP_IN_A_LEVEL = 50

class Player:
    # set of all possible player actions
    # irrelevant set, i'm gonna keep it just in case but for now it's gonna stay commented out 
    # PLAYER_ACTIONS = {"CHECK", "ATTACK", "EQUIP", "TOSS", "BUY", "SELL"}

    def __init__(self, name:str, stats_filepath:str = "dictionaries/player_stats.txt"):
        self.name = name
        self.stats = {}

        # NOTE: There is 50 exp contained in 1 level 
        self.level = 1
        self.exp_total = 0

        self.gold = 0

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
        return f"You are {self.name}.\nYou are level {self.level} and have {self.exp_total} experience points.\nYou currently have a(n) {self.equipped_weapon.get_name()} equipped.\nYou have {self.gold} gold."

    # converts the inventory array into a string that looks prettier for printing 
    def inventory_as_str(self) -> str:
        output = []

        for i in self.inventory:
            output.append(i.get_name())

        return list_to_string(output)

    def add_gold(self, gold:int) -> None:
        self.gold += gold 


    def add_exp(self, exp:int) -> None:
        self.exp_total += exp

        num_levels_gained = self.exp_total // EXP_IN_A_LEVEL 
        self.exp_total -= (EXP_IN_A_LEVEL * num_levels_gained)

        self.level += num_levels_gained

        if num_levels_gained > 0:
            print(f"You gained {num_levels_gained} levels!")

            # TODO: Update stats on level up