"""
4/22/2025
David Knowles

File that handles room actions
"""

from mapgeneration import *
from player import Player 

from common_funcs import *

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
