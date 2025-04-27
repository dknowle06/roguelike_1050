"""
David Knowles 
4/26/2025
File that stores the main gameloop
This is the file that should be run if you want to play the game!!!!!!!!!!!!!!!!!

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
from room_handler import *

DEBUG = False

if __name__ == "__main__":
    # used to measure the amount of time it takes to setup the program
    start_time = time.time()

    # take a command line argument to initialize the seed 
    # if no argument is provided, generate a random seed
    args = sys.argv[1:]

    seed = 0

    # if the command line arguments contain a seed, set the seed to that 
    # else, generate a seed using the time and a weird bitwise formula 
    if len(args) > 0:
        mpgt.set_seed(args[0])
        seed = args[0]
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
            print(dungeon_map.parent_dictionary[key].get_data().get_encounter().elements + dungeon_map.parent_dictionary[key].get_data().get_encounter().treasure)

        print(f"DUNGEON MAP LENGTH = {len(dungeon_map)}")

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
    player_obj.set_equipped_weapon(0)
    newline()

    # prints the player stats
    print(player_obj)

    # displays the dungeon map
    print(f"\nDungeon map:\n{mpgt.dungeon_map_to_string(dungeon_map)}\n")

    # `player_position` stores the position of the player. directly comparable to the room ids in the dungeon_map
    player_position = 0
    gameloop = True

    # assumes the player has died until explicitly told the player has not died
    player_died = True

    output = ""


    while gameloop:
        current_room = dungeon_map.get_node_from_id(player_position).get_data()
        room_id = current_room.get_id()

        gameloop = room_handler(current_room, player_obj, mpgt.dungeon_map_to_string(dungeon_map, player_position), dungeon_map)

        # exits the game loop if the player is dead
        if gameloop == False:
            break

        gathering_input = True
        # sets up an array of room objects, this array will contain the next availabe rooms that the player can traverse to
        next_rooms = [x.get_data() for x in dungeon_map.get_node_from_id(player_position).get_children()]

        # only allows the player to progress if the player is not at the end of the dungeon
        if player_position < len(dungeon_map) - 1:
            # gathers input, will end when the user chooses to continue to the next room
            while gathering_input:
                print("What do you want to do?")

                user_input = input_validation("",VALID_ACTION, lambda a: a.split()[0] in NAVIGATION_COMMS)

                gathering_input = not input_handler(user_input, next_rooms, player_obj, mpgt.dungeon_map_to_string(dungeon_map, player_position))
                
            # the second element in `next_rooms` will be updated by `gathering_input`
            # this element will be a value used to shift the player's position into the room they chose 
            player_position += next_rooms[1]
        else:
            newline(2)

            output += "Congratulations! You beat the game!\n"
            output += str(player_obj) + "\n\n"
            output += f"Inventory: {player_obj.inventory_as_str()}\n\n"
            output += f"{mpgt.dungeon_map_to_string(dungeon_map)}\n\n"
            output += f"\nRun Seed: {seed}"

            print(output)

            gameloop = False
            player_died = False

    if player_died:
        newline(2)

        output += "You have died! GG\n\n"
        output += str(player_obj) + "\n\n"
        output += f"Inventory: {player_obj.inventory_as_str()}\n\n"
        output += f"{mpgt.dungeon_map_to_string(dungeon_map)}\n\n"
        output += f"\nRun Seed: {seed}"

        print(output)

    newline(2)
    print("Check `game_results.txt` for your end-of-game results!")
    print("*Note*\n\tThere is currently an issue with how the ascii art for the map gets rendered in the output file. Please ignore that! I'm not exactly sure how to fix it or what the issue is.\n")

    # outputs the game results to a file after the player has beat the game or after the player has died
    with open("game_results.txt", "w") as f:
        f.write(output)