# David Knowles
# 4/8/2025
# testing for dictionary parsing and initializing game objects

from dict_parser import dict_parser
from game_object import Enemy
from game_object import Item

if __name__ == "__main__":
    enemies = dict_parser("dictionaries/enemies.txt", ":", True)

    test_enemy = Enemy(enemies[1])

    print(test_enemy)

    print(test_enemy.attack()(test_enemy.stats,test_enemy.name))