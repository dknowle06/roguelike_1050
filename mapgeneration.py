"""
David Knowles
4/2/2025

Contains functions and classes used for generating maps and storing rooms 
"""

from nodetree import Tree
from random import randint
from random import seed as random_seed

# returns a random element from the list, and pops it
# returns `None` if the list is empty
def rand_element(listparam:list):
    return listparam.pop(randint(0, len(listparam) - 1)) if len(listparam) > 0 else None

# literally just an alias for `random.seed(n)`
def set_seed(seed:int = 0):
    random_seed(seed)

# class that stores all possible room types, and associates them with an integer
# kind of like a faux-enum, since python enums require importing a library for some reason 
class ROOM_TYPES:
    FIGHT = 0
    BOSS = 1
    MINIBOSS = 2
    TREASURE = 10
    SHOP = 20
    FOUNTAIN = 300

TESTING = True

class Encounter:
    # class that generates an encounter for a room

    # `self.elements` stores the enemies or items used during the encounter

    # lists that store data pertaining to enemies, minibosses, bosses, and items
    # will store dictionaries, "var_name":var_data, where "var_name" is a string 
    # will be initialized from a .txt file
    enemy_data = []
    miniboss_data = []
    boss_data = []
    item_data = []

    # room_type should be:
    # 0 - FIGHT
    # 1 - BOSS
    # 2 - MINIBOSS
    @staticmethod
    def enemy_generator(room_type:int = 0) -> list:
        enemy_list = []

        return enemy_list

    @staticmethod
    def item_generator(room_type:int = 0) -> list:
        item_list = []

        return item_list


    def __init__(self, room_id:int = 0):
        # TODO:
        # - create a function that generates enemies, will be reused for fight, boss, and miniboss

        # - create a function that generates a set of items, will be reused for treasure and shop

        # - define fountain

        self.elements = []
        
        if (room_id in {ROOM_TYPES.FIGHT, ROOM_TYPES.BOSS, ROOM_TYPES.MINIBOSS}):
            self.elements = enemy_generator(room_id)
        elif (room_id in {ROOM_TYPES.TREASURE, ROOM_TYPES.SHOP}):
            self.elements = item_generator(room_id)
        elif (room_id == ROOM_TYPES.FOUNTAIN):
            pass
        else: # handle bad input
            pass

class Room:
    """
    `room_id` stores the type of room
    `this_encounter` stores the encounter
    """

    IDS_ROOMS = {
        ROOM_TYPES.FIGHT:"Enemy Encounter",
        ROOM_TYPES.BOSS:"Boss Encounter",
        ROOM_TYPES.MINIBOSS:"Miniboss Encounter",
        ROOM_TYPES.TREASURE:"Treasure Room",
        ROOM_TYPES.SHOP:"Shop",
        ROOM_TYPES.FOUNTAIN:"Healing Fountain"
    }

    def __init__(self, room_id:int = 0):
        self.room_id = room_id
        self.this_encounter = Encounter(self.room_id)

    def __str__(self) -> str:
        return f"{IDS_ROOMS[self.room_id]}"

# returns a `Tree`
"""
Each map will have 12 levels, with 18 total rooms
1 2-way split path with 2 levels
1 3-way split path with 2 levels 
First level is a fight
Last level is a boss fight
"""
def create_map():
    twosplit_loc   = []
    threesplit_loc = []

    # used to decide which levels will have a split path
    undecided_rooms = list(range(1,10))

    # place the 2-way split
    room_num = rand_element(undecided_rooms)
    twosplit_loc.append(room_num)
    twosplit_loc.append(room_num + 1)

    # ensures that the split paths are placed a reasonable length apart 
    remover_list = [-2, -1, 1, 2]
    for remover in remover_list:
        if room_num + remover in undecided_rooms:
            undecided_rooms.remove(room_num + remover)

    # place the 3-way split
    room_num = rand_element(undecided_rooms)
    threesplit_loc.append(room_num)
    threesplit_loc.append(room_num + 1)

    # dictionary used to associate room ids with room type
    # techincally, with how i implement this, i think an array would functionally do the same thing. but this also works just fine
    # and is probably a little more readable and clear as to what it does?
    # forces the first room to always be a fight
    room_dict = {
        0:ROOM_TYPES.FIGHT
    }

    # creates a list of available room types to be used when setting up `room_dict`
    available_rooms = [ROOM_TYPES.FOUNTAIN]
    for i in range(2):
        available_rooms.append(ROOM_TYPES.MINIBOSS)
        available_rooms.append(ROOM_TYPES.TREASURE)
        available_rooms.append(ROOM_TYPES.SHOP)

    for i in range(9):
        available_rooms.append(ROOM_TYPES.FIGHT)

    # sets room 1 - 16
    for i in range(1,17):
        room_dict[i] = rand_element(available_rooms)

    # sets room 17 to a boss fight 
    room_dict[17] = ROOM_TYPES.BOSS

    # prints debug info
    if TESTING:
        print(room_dict, len(room_dict))
        print(f"twosplit_loc: {twosplit_loc}, threesplit_loc: {threesplit_loc}")

    # when doing splits:
    # room ids are assigned by row, starting at the top row 

    generated_map = Tree(room_dict[0])

    # stores which room to use
    counter = 1

    # used to store the parents of the new node
    previous = [0]
    for i in range(1,10):
        # stores the parents for the next node
        current_ids = []

        # two way split
        if i == twosplit_loc[0]:

            for i in range(2):
                generated_map.add_node(room_dict[counter], previous)
                generated_map.add_node(room_dict[counter + 1], [counter])

                counter += 2
                current_ids.append(counter - 1)

        # three way split
        elif i == threesplit_loc[0]:

            for i in range(3):
                generated_map.add_node(room_dict[counter], previous)
                generated_map.add_node(room_dict[counter + 1], [counter])

                counter += 2
                current_ids.append(counter - 1)

        # linear
        else:
            generated_map.add_node(room_dict[counter], previous)

            current_ids = [counter]
            counter += 1

        previous = current_ids

    # prints MORE debug info
    # helps ensure that the tree is of a proper length, should be 18 as of 3/26/2025
    if TESTING:
        print("genmap len =", len(generated_map))
    
    return generated_map