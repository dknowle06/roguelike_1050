"""
David Knowles 
4/16/2025
File that stores the main gameloop

This is like if balatro was a dungeon crawler and also made by someone who doesn't really understand game design
Game's title is currently 1050 Roguelike, I can't think of anything else better
"""

import mapgeneration as mpgt
from player import Player

import sys # used to grab command line arguments 
import time # used for random seed generation


# prints `num` newlines
def newline(num:int = 1):
    for i in range(num):
        print()

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

    # loads game objects into memory
    print("Loading game objects...")
    mpgt.Encounter.load_object_data()
    
    print("Generating dungeon map...")
    dungeon_map = mpgt.create_map()

    print(f"Game setup completed in {time.time() - start_time} seconds.")

    # prints title 
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

    print(player_obj)