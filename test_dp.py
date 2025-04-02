# David Knowles
# 4/2/2025
# testing for dictionary parsing and initializing game objects

from dict_parser import dict_parser
from game_object import Enemy
from game_object import Item

if __name__ == "__main__":
    a = dict_parser("dictionaries/testing/enemy_test.txt", clean_key = True)

    enemy_test = Enemy(a[0])

    print(enemy_test)

    print("\n")

    b = dict_parser("dictionaries/testing/item_test.txt", clean_key = True)

    item_test = Item(b[0])

    print(item_test)