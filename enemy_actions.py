"""
David Knowles
4/26/2025

Contains functions that return `Enemy_Action` objects
These objects contain information about stat boosts, healing, damage, etc. 
"""

# NOTE! randint is inclusive from a to b
from random import randint 

# consts that store damage types
PHYSICAL = 1
SPECIAL  = 2
PIERCING = 3

"""
Physical damage is damage dealt with regular weapons

Special damage is damage dealt with magic 

Piercing damage is damage that ignores player and enemy stats 
"""

# converts the damage type integers to strings
def get_damage_type(damage_type:int) -> str:

    if damage_type == PHYSICAL:
        return "regular"
    elif damage_type == SPECIAL:
        return "magic"
    elif damage_type == PIERCING:
        return "piercing"

    return "NULL"

class Enemy_Action:

    # TODO:
    # add status effects as a thing, and add `*args`` before the `**kwargs`` to take in status effects

    # healing and damage are self explanatory
    # **kwargs contains all stat boosts
    # wow an actual use for kwargs, CRAZY
    def __init__(self, healing:float, damage:float, enemy_name:str, attack_verb:str, damage_type:int = PHYSICAL):
        self.healing = healing
        self.damage = damage

        self.enemy_name = enemy_name
        self.attack_verb = attack_verb

        self.stat_boosts = {}

        self.damage_type = damage_type

    # string :-)
    def __str__(self) -> str:
        output_str = f"{self.enemy_name} {self.attack_verb}!\n"

        if self.damage != 0:
            output_str += f"{self.enemy_name} hit you for {self.damage:.1f} {get_damage_type(self.damage_type)} damage." if self.damage > 0 else f"{self.enemy_name} healed you for {-1 * self.damage:.1f} hp."
            output_str += "\n"

        if self.healing != 0:
            output_str += f"{self.enemy_name} healed itself for {self.healing:.1f} hp." if self.healing > 0 else f"{self.enemy_name} dealt {-1 * self.healing:.1f} damage to itself."
            output_str += "\n"

        return output_str[:-1]

    # modifies the damage amount based on enemy and player stats
    def mod_damage(self, player_stats:dict) -> None:

        # realistically i should be using try/catch here to be safe
        # but if these aren't defined in the dictionaries passed, there is a major issue happening somewhere else
        # essentially, not this function's problem!!!
        player_defense = player_stats["Defense"]
        player_sp_defense = player_stats["Special Defense"]

        # ends the function execution if the enemy is actually healing the player, or if the enemy deals no damage
        if self.damage <= 0:
            return None

        # decrease damage based on player defense stat

        # don't modify piercing damage!! 

        if self.damage_type == PHYSICAL:
            self.damage = self.damage / ((player_defense + 100) / 100)

        elif self.damage_type == SPECIAL:
            self.damage = self.damage / ((player_sp_defense + 100) / 100)

    def get_healing(self) -> float:
        return self.healing
    
    def get_damage(self) -> float:
        return self.damage



# FUNCTION SECTION
# all functions should be defined as:
"""
def foo(stats_dict:dict, enemy_name:str):
    *math stuff here*
    return `Enemy_Action`
"""

# healing, damage, enemy name, attack verb


def flop(stats_dict:dict, enemy_name:str):
    return Enemy_Action(0, 1, enemy_name, "flopped around", PHYSICAL)

def cough(stats_dict:dict, enemy_name:str):
    return Enemy_Action(-2, 0, enemy_name, "coughed", PHYSICAL)

def sneeze(stats_dict:dict, enemy_name:str):
    return Enemy_Action(-1, 1, enemy_name, "sneezed", PIERCING)

def bash_attack(stats_dict:dict, enemy_name:str):
    enemy_attack = stats_dict["Attack"]

    damage = 2.7 * (enemy_attack + 100) / 100
    return Enemy_Action(0, damage, enemy_name, "bashed you", PHYSICAL)

def curse_attack(stats_dict:dict, enemy_name:str):
    enemy_attack = stats_dict["Special Attack"]

    damage = 2.7 * (enemy_attack + 100) / 100
    return Enemy_Action(0, damage, enemy_name, "placed a curse on you", SPECIAL)

def heal_spell(stats_dict:dict, enemy_name:str):
    return Enemy_Action(float(randint(1,5)), 0, enemy_name, "casted a spell to heal itself", SPECIAL)

# FUNCTION DICTIONARY
ENEMY_ACTIONS_DICT = {
    "flop":flop,
    "cough":cough,
    "sneeze":sneeze,
    "bash":bash_attack,
    "curse":curse_attack,
    "heal_spell":heal_spell
}