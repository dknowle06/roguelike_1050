"""
David Knowles
4/2/2025

Contains functions that return `Enemy_Action` objects
These objects contain information about stat boosts, healing, damage, etc. 

"""

class Enemy_Action:

    # healing and damage are self explanatory
    # **kwargs contains all stat boosts
    # wow an actual use for kwargs, CRAZY
    def __init__(self, healing:float, damage:float, enemy_name:str, attack_verb:str, **kwargs):
        self.healing = healing
        self.damage = damage

        self.enemy_name = enemy_name
        self.attack_verb = attack_verb

        self.stat_boosts = {}
        
        for key, value in kwargs.items():
            # using the type casts i define in `Stat_Boost` here instead of normal getters or setters
            # probably not as clear in the code for what it does but it's a little more concise i think 
            self.stat_boosts[key] = value

    def __str__(self) -> str:
        output_str = f"{self.enemy_name} {self.attack_verb}!\n"

        if self.damage != 0:
            output_str += f"{self.enemy_name} hit you for {self.damage} damage." if self.damage > 0 else f"{self.enemy_name} healed you for {-1 * self.damage} hp."
            output_str += "\n"

        if self.healing != 0:
            output_str += f"{self.enemy_name} healed itself for {self.healing} hp." if self.healing > 0 else f"{self.enemy_name} dealt {-1 * self.healing} damage to itself."
            output_str += "\n"

        return output_str[:-1]


# FUNCTION SECTION
# all functions should be defined as:
"""
def foo(stats_dict:dict, enemy_name:str):
    \*math stuff here\*
    return `Enemy_Action`
"""

# healing, damage, enemy name, attack verb, status effects (TODO), stat buffs


def flop(stats_dict:dict, enemy_name:str):
    return Enemy_Action(0, 1, enemy_name, "flopped around")

def cough(stats_dict:dict, enemy_name:str):
    return Enemy_Action(-1, 0, enemy_name, "coughed")

# FUNCTION DICTIONARY
ENEMY_ACTIONS_DICT = {
    "flop":flop,
    "cough":cough
}