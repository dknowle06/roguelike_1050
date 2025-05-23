"""
David Knowles
4/28/2025

Contains functions and classes used for generating maps and storing rooms 
Stores the Encounter and the Room class 
"""

from nodetree import Tree
# NOTE! randint is inclusive from a to b
from random import randint 
from random import seed as random_seed
from dict_parser import dict_parser
from game_object import Enemy
from game_object import Item
import copy

# returns a random element from the list, and pops it
# returns `None` if the list is empty
def rand_element(listparam:list):
    return listparam.pop(randint(0, len(listparam) - 1)) if len(listparam) > 0 else None

# initializes the seed and prints out the seed
# prints an error message if the seed isn't an integer
def set_seed(seed = 0):
    try:
        seed = int(seed)

        random_seed(seed)
        print(f"Seed set to {seed}.")
    except ValueError as e:
        print(e)
        print(f"Seed {seed} not of type `int`.")
        quit()

# class that stores all possible room types, and associates them with an integer
# kind of like a faux-enum, since python enums require importing a library for some reason 
class ROOM_TYPES:
    FIGHT = 0
    BOSS = 1
    MINIBOSS = 2
    TREASURE = 10
    SHOP = 20
    FOUNTAIN = 300

TESTING = False

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

    # function that initializes the databases of enemies, minibosses, bosses, and items from the dictionary files
    def load_object_data() -> None:
        # initialize enemies
        enemy_temp = dict_parser("dictionaries/enemies.txt", ":", True)
        Encounter.enemy_data = [Enemy(x) for x in enemy_temp]
        print("Enemies initialized!")

        miniboss_temp = dict_parser("dictionaries/minibosses.txt", ":", True)
        Encounter.miniboss_data = [Enemy(x) for x in miniboss_temp]
        print("Minibosses initialized!")

        boss_temp = dict_parser("dictionaries/bosses.txt", ":", True)
        Encounter.boss_data = [Enemy(x) for x in boss_temp]
        print("Bosses initialized!")
        
        # initialize items
        item_temp = dict_parser("dictionaries/weapons.txt", ":", True)
        item_temp += dict_parser("dictionaries/consumables.txt", ":", True)
        Encounter.item_data = [Item(x) for x in item_temp]

        # add items to item dictionary
        for i in Encounter.item_data:
            Item.update_item_dict(i)

        print("Items initialized!")

    # room_type should be:
    # 0 - FIGHT
    # 1 - BOSS
    # 2 - MINIBOSS
    def enemy_generator(room_type:int = ROOM_TYPES.FIGHT) -> list:
        enemy_list = []

        if room_type == ROOM_TYPES.FIGHT:

            # this could originally generate up to 3 enemies, but that would very easily overwhelm the player
            # so it can now only generate up to 2 enemies
            # i kind of realized how messed up the balance of my game is, so i changed it back to 3 so it could be a bit harder
            num_enemies = randint(1,3)

            for i in range(num_enemies):
                # gross syntax, but just grabs a random element from `Encounter.enemy_data` and copies it 
                enemy_list.append(copy.deepcopy(Encounter.enemy_data[randint(0, len(Encounter.enemy_data) - 1)]))

        # these all do the same thing as above but for their respective data type 

        elif room_type == ROOM_TYPES.MINIBOSS:
            enemy_list.append(copy.deepcopy(Encounter.miniboss_data[randint(0, len(Encounter.miniboss_data) - 1)]))

        elif room_type == ROOM_TYPES.BOSS:
            enemy_list.append(copy.deepcopy(Encounter.boss_data[randint(0, len(Encounter.boss_data) - 1)]))

        return enemy_list

    def item_generator(room_type:int = 0) -> list:
        item_list = []

        # gives 5 items for a shop
        # gives 2 items for anything else (in practice, this will be for miniboss encounters and treasure rooms)
        num_items = 5 if room_type == ROOM_TYPES.SHOP else 2

        for i in range(num_items):
            item_list.append(copy.deepcopy(Encounter.item_data[randint(0, len(Encounter.item_data) - 1)]))


        return item_list


    def __init__(self, room_id:int = 0):
        # TODO:
        # - create a function that generates enemies, will be reused for fight, boss, and miniboss (DONE!)

        # - create a function that generates a set of items, will be reused for treasure and shop, as well as minibosses

        # - define fountain (DONE!)

        self.elements = []
        self.treasure = []
        
        if (room_id in {ROOM_TYPES.FIGHT, ROOM_TYPES.BOSS, ROOM_TYPES.MINIBOSS}):
            self.elements = Encounter.enemy_generator(room_id)

            # adds a bonus item to be awarded to the player upon clearing a miniboss/boss room 
            if (room_id in {ROOM_TYPES.MINIBOSS}):
                self.treasure = Encounter.item_generator(room_id)
                
        elif (room_id in {ROOM_TYPES.TREASURE, ROOM_TYPES.SHOP}):
            self.elements = Encounter.item_generator(room_id)
        elif (room_id == ROOM_TYPES.FOUNTAIN):
            # if `self.elements` is an array of length 1 with only an integer, it can be assumed that it is a fountain room 
            self.elements = [ROOM_TYPES.FOUNTAIN] 
        else: # handle bad input
            # print an error message and then exits the program 
            print(f"Error: Bad `ROOM_TYPE`: {room_id}.")
            quit()

    def get_elements(self) -> list:
        return self.elements

    def get_treasure(self) -> list:
        return self.treasure

    # function used for testing
    # displays the elements within an encounter
    # might be reworked to be used within a final build later on?
    def element_names(self) -> str:
        output = ""
        for i in self.elements:
            output += f"{i.get_name()}, "

        return output[:-2]

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
        return f"{Room.IDS_ROOMS[self.room_id]}"

    def get_encounter(self):
        return self.this_encounter
    
    def get_id(self):
        return self.room_id

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
    # NOTE: On 4/21/2025 I changed the upper bound from 10 to 9. A bug involving generating a two-way split as the last set was discovered
    # To remedy this, I lowered the range in which splits can be placed. 
    undecided_rooms = list(range(1,9))

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

    print("Room IDs Set!")

    # prints MORE debug info
    # helps ensure that the tree is of a proper length, should be 18 as of 3/26/2025
    if TESTING:
        print("genmap len =", len(generated_map))
        print(generated_map)
    
    return generated_map

# takes a tree of room ids and converts it to room objects
def modify_map(dungeon_map_ids):
    dungeon_map = copy.deepcopy(dungeon_map_ids)

    # converts room ids to proper encounters 
    for key in dungeon_map.parent_dictionary:
        room_id_temp = dungeon_map.parent_dictionary[key].get_data() # gets the room id stored at the room index
        dungeon_map.parent_dictionary[key].data = Room(room_id_temp) # replaces the room id with an encounter 

    print("Encounter + Room data generated!")

    return dungeon_map

# id used to determine the position of a player
# value is arbitray, i just went with 2025 bc that's the year  
PLAYER_HERE = 2025

# dictionary used when printing a dungeon map
# converts dungeon ids to relevant symbols 
ID_TO_SYMBOL = {
    ROOM_TYPES.FIGHT: "F",
    ROOM_TYPES.BOSS: "B",
    ROOM_TYPES.MINIBOSS: "M",
    ROOM_TYPES.TREASURE: "X",
    ROOM_TYPES.SHOP: "$",
    ROOM_TYPES.FOUNTAIN: "H",
    PLAYER_HERE: "O"
}

# converts a dungeon map to a string that can be printed
# player position tells the function where the player is, and returns "O" at the player's position
def dungeon_map_to_string(dungeon_map, player_position:int = -1) -> str:
    id_dict = copy.deepcopy(dungeon_map.parent_dictionary) # copied since an id may need to be changed 

    if player_position in range(0,18):
        id_dict[player_position].data.room_id = PLAYER_HERE

    top_row = ""
    middle_row = ""
    bottom_row = ""

    idx = 0

    # i do sincerely apologize for this function's implementation. 
    # i did not design this for reusability, or scalability. the map size for printing is hardcoded at 18
    # for the functionality of this program. this is fine. i could rework it if needed, but otherwise this is good enough

    while idx < 18:
        num_children = len(id_dict[idx].get_children())

        # final boss
        if num_children == 0:
            middle_row += ID_TO_SYMBOL[id_dict[idx].get_data().get_id()]
        
        # straight path
        elif num_children == 1:
            middle_row += ID_TO_SYMBOL[id_dict[idx].get_data().get_id()] + " - "
            top_row += "    "
            bottom_row += "    "

        # two-way split path
        elif num_children == 2:
            middle_row += ID_TO_SYMBOL[id_dict[idx].get_data().get_id()] + "          "

            top_row += f"  / {ID_TO_SYMBOL[id_dict[idx + 1].get_data().get_id()]} - {ID_TO_SYMBOL[id_dict[idx + 2].get_data().get_id()]} \\"
            bottom_row += f"  \\ {ID_TO_SYMBOL[id_dict[idx + 3].get_data().get_id()]} - {ID_TO_SYMBOL[id_dict[idx + 4].get_data().get_id()]} /"

            idx += 4

        # three-way split path
        elif num_children == 3:
            middle_row += f"{ID_TO_SYMBOL[id_dict[idx].get_data().get_id()]} - {ID_TO_SYMBOL[id_dict[idx + 3].get_data().get_id()]} - {ID_TO_SYMBOL[id_dict[idx + 4].get_data().get_id()]} - "

            top_row += f"  / {ID_TO_SYMBOL[id_dict[idx + 1].get_data().get_id()]} - {ID_TO_SYMBOL[id_dict[idx + 2].get_data().get_id()]} \\"
            bottom_row += f"  \\ {ID_TO_SYMBOL[id_dict[idx + 5].get_data().get_id()]} - {ID_TO_SYMBOL[id_dict[idx + 6].get_data().get_id()]} /"

            idx += 6


        idx += 1

        
    middle_border = ""
    for i in range(47):
        middle_border += "-"

    output = f"/{middle_border}\\\n| {top_row}    |\n| {middle_row}  |\n| {bottom_row}    |\n\\{middle_border}/"
    return output