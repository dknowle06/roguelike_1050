# David Knowles
# 4/2/2025
# testing for dictionary parsing and initializing game objects

from dict_parser import dict_parser
from game_object import Enemy
from game_object import Item

if __name__ == "__main__":
    enemies = dict_parser("dictionaries/enemies.txt", ":", True)

    magical_carp = Enemy(enemies[0])

    print(magical_carp)

    print(magical_carp.attack()(magical_carp.stats,magical_carp.name))