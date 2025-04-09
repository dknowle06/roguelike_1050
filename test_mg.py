# David Knowles
# 4/9/2025
# testing for map generation

from mapgeneration import *

# executes code only inside of this `if` statement
if __name__ == "__main__":
    Encounter.load_object_data()

    for enemy in Encounter.enemy_data:
        print(f"{enemy}\n")