"""
David Knowles 
4/14/2025
File that stores the main gameloop
"""

import mapgeneration as mpgt
import sys # used to grab command line arguments 
import time # used for random seed generation

if __name__ == "__main__":
    # take a command line argument to initialize the seed 
    # if no argument is provided, generate a random seed
    args = sys.argv[1:]

    if len(args) > 0:
        mpgt.set_seed(args[0])
    else:
        # seed generation formula shamelessly stolen from stack overflow
        # https://stackoverflow.com/questions/27276135/python-random-system-time-seed
        t = int(time.time() * 1000)
        # used funny bitwise arithmetic that i only half understand... yippee!!
        # makes the generated seed feel more "random", as apposed to just using the time to make the seed
        seed = ((t & 0xff000000) >> 24) + ((t & 0x00ff0000) >>  8) + ((t & 0x0000ff00) <<  8) + ((t & 0x000000ff) << 24)
        mpgt.set_seed(seed)