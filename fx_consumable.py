"""
David Knowles
4/26/2025

contains actions for consumable items
"""

from player import Player


# FUNCTION SECTION
# all functions should be defined as:
"""
def foo(player, enemies:list):
    *do item action here*

    print("Whatever the item did.")
"""

def heal_cs(player, enemies:list):
    player.get_stats()["Hp"] += 10.0

    print("Healed 10.0 HP!")

CONSUMABLE_FX_DICT = {
    "heal_cs":heal_cs
}