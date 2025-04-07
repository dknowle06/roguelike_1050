"""
David Knowles 
4/7/2025
Class containing player information
"""

from dict_parser import dict_parser

class Player:
    def __init__(self, name:str, stats_filepath:str = "dictionaries/player_stats.txt"):
        self.name = name

        self.stats = dict_parser(stats_filepath)
        # used to store status effects
        self.temp_stats = {}

    def get_stats(self) -> dict:
        return self.stats