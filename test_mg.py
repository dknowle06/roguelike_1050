# David Knowles
# 4/9/2025
# testing for map generation

from mapgeneration import *
from game_object import *

# executes code only inside of this `if` statement
if __name__ == "__main__":
    Encounter.load_object_data()

    set_seed(1)

    test_room = Encounter(ROOM_TYPES.FIGHT)

    print(test_room.element_names())

    test_item = Item.get_item_from_dict("rusty dagger")
    print(test_item)