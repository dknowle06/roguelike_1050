"""
David Knowles 
4/22/2025
File that stores the main gameloop

This is like if balatro was a dungeon crawler and also made by someone who doesn't really understand game design but has played way too much balatro
Game's title is currently 1050 Roguelike, I can't think of anything else better

Check https://stackoverflow.com/questions/27276135/python-random-system-time-seed for an algorithm I used for random seed generation

I apologize for my spaghetti code!!! The scope of this project is much larger than anything else I've written before.
"""

import mapgeneration as mpgt
from mapgeneration import ROOM_TYPES
from player import Player

import sys # used to grab command line arguments 
import time # used for random seed generation and printing load times 

from common_funcs import *


# sets that store valid player commands 
# `EVERYDAY_COMMS` shouldn't be used, it's only here to be unioned to create the attack and shop command sets 
EVERYDAY_COMMS = {"CHECK", "EQUIP", "TOSS", "USE"}
ATTACK_COMMS = EVERYDAY_COMMS | {"ATTACK"}
SHOP_COMMS = EVERYDAY_COMMS | {"BUY", "SELL"}
NAVIGATION_COMMS = EVERYDAY_COMMS | {"NEXT", "CONTINUE"} # next and continue will do the same thing 

DEBUG = True

if __name__ == "__main__":
    # used to measure the amount of time it takes to setup the program
    start_time = time.time()

    # take a command line argument to initialize the seed 
    # if no argument is provided, generate a random seed
    args = sys.argv[1:]

    # if the command line arguments contain a seed, set the seed to that 
    # else, generate a seed using the time and a weird bitwise formula 
    if len(args) > 0:
        mpgt.set_seed(args[0])
    else:
        # seed generation formula shamelessly stolen from stack overflow
        # https://stackoverflow.com/questions/27276135/python-random-system-time-seed
        t = int(time.time() * 1000) # i have to cast to int here since bitwise operators don't work on floats 
        # used funny bitwise arithmetic that i only half understand... yippee!!
        # to my understanding it shuffles the order of the bytes:
        # int ABCD ==> int DCBA (i think)
        # makes the generated seed feel more "random", as apposed to just using the time to make the seed
        seed = ((t & 0xff000000) >> 24) + ((t & 0x00ff0000) >>  8) + ((t & 0x0000ff00) <<  8) + ((t & 0x000000ff) << 24)
        mpgt.set_seed(seed)

        # NOTE: I've noticed that bizzarely, the seeds seem to always be an odd integer (i'm struggling to find an even seed in my tests). 
        # this does work to my favor, since odd numbers do feel more "random" than even integers

    # loads game objects into memory
    print("Loading game objects...")
    mpgt.Encounter.load_object_data()
    
    print("Generating dungeon map...")
    # creates a dungeon map of ids, and then converts the id map to a room map
    dungeon_map = mpgt.modify_map(mpgt.create_map())

    # prints dungeon map object data if debugging
    if DEBUG:
        for key in dungeon_map.parent_dictionary:
            print(f"{key}:{dungeon_map.parent_dictionary[key]}")

        for key in dungeon_map.parent_dictionary:
            print(dungeon_map.parent_dictionary[key].get_data().get_encounter().elements)

    print(f"Game setup completed in {time.time() - start_time} seconds.")

    # prints title 
    # the for loops print dashes, because i'm too lazy to type out 30 dashes 
    print("\n\n")
    for i in range(2):
        print("\t", end="")
        for i in range(30):
            print("-", end="")

        newline()

    print("\t-~Welcome to 1050 Roguelike!~-")

    for i in range(2):
        print("\t", end="")
        for i in range(30):
            print("-", end="")

        newline()

    newline(2)

    # get player name
    print("What is the adventurer's name?")
    username = input().title()

    player_obj = Player(username,"dictionaries/player_stats.txt")
    newline()

    # prints the player stats
    print(player_obj)

    # displays the dungeon map
    print(f"\nDungeon map:\n{mpgt.dungeon_map_to_string(dungeon_map)}\n")

    # `player_position` stores the position of the player. directly comparable to the room ids in the dungeon_map
    player_position = 0
    gameloop = True

    while gameloop:
        current_room = dungeon_map.get_node_from_id(player_position).get_data()
        room_id = current_room.get_id()

        if room_id == ROOM_TYPES.FIGHT:
            enemies = current_room.get_encounter().get_elements()
            enemy_names = [x.get_name() for x in enemies]

            print(f"You enter a room, and get ambushed by some enemies:")
            print(list_to_string(enemy_names))

            print("What do you want to do?")

            user_action = input_validation(f"", "Please choose a valid action!\n", lambda a: a in ATTACK_COMMS)

