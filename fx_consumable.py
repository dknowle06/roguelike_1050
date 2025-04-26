"""
David Knowles
4/26/2025

contains actions for consumable items
"""

from common_funcs import DEFAULT_STAT_LIST
# NOTE! randint is inclusive from a to b
from random import randint 

# NOTE: importing player is unnecessary since python just like... doesn't care if you call a function that hasn't really been well defined?
# for example, in `heal_cs` i use player.get_stats(), but technically speaking, this file doesn't know what get_stats does or what class it belongs to 
# how is this allowed????????
# if i had to guess, what i'm doing here is HORRIBLE HORRIBLE practice, and if you're reading this... look away!!!
# anywho, the main reason I'm not importing player here is due to the program immediately crashing if i do that due to a circular import... and i'm too tired to figure that out

# FUNCTION SECTION
# all functions should be defined as:
"""
def foo(player, enemies:list) -> bool:
    *do item action here*

    print("Whatever the item did.")

    return turn continue value
"""

END_TURN = True
CONTINUE_TURN = False

def heal_cs(player, enemies:list) -> bool:
    player.get_stats()["Hp"] += 10.0

    print("Healed 10.0 HP!")

    return END_TURN

def gros_michel(player, enemies:list) -> bool:
    # picks the index for which stat to upgrade
    stat_id = randint(0, len(DEFAULT_STAT_LIST) - 1)
    # decides whether or not to destroy gros michel
    # destroys gros michel if 0 is rolled
    destroyed = True if randint(0,5) == 0 else False

    player.get_stats()[DEFAULT_STAT_LIST[stat_id]] += 1.5
    print(f"Permanently boosted {DEFAULT_STAT_LIST[stat_id]} by 1.5!")

    if not destroyed:
        player.add_item_from_str("gros michel")
    else:
        print("Gros Michel was destroyed!")
        return END_TURN

    return CONTINUE_TURN

# used to assign functions to consumables
CONSUMABLE_FX_DICT = {
    "heal_cs":heal_cs,
    "gros_michel":gros_michel
}