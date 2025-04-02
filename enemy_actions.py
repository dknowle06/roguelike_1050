"""
Contains functions that return `Enemy_Action` objects
These objects contain information about stat boosts, healing, damage, etc. 

"""

# literally just a string/float pair
# kinda unnecessary for me to define this class but wtvr
class Stat_Boost:
    def __init__(self, str_:str, float_:float):
        self.str_ = str_ 
        self.float_ = float_

    def __str__(self) -> str:
        return self.str_
    
    def __float__(self) -> float:
        return self.float_


class Enemy_Action:

    # healing and damage are self explanatory
    # *args contains all the stat boosts that will be added to the `stat_boosts` dictionary
    # *args should be of type `Stat_Boost`
    def __init__(self, healing:float, damage:float, *args):
        self.healing = healing
        self.damage = damage

        self.stat_boosts = {}
        
        for arg in args:
            # using the type casts i define in `Stat_Boost` here instead of normal getters or setters
            # probably not as clear in the code for what it does but it's a little more concise i think 
            self.stat_boosts[str(arg)] = float(arg)


# FUNCTION SECTION
# all functions should be defined as:
"""
def foo(stats_dict:dict):
    \*math stuff here\*
    return `Enemy_Action`
"""


def flop(stats_dict:dict):
    return Enemy_Action(0, 1)

# FUNCTION DICTIONARY
ENEMY_ACTIONS_DICT = {
    "flop":flop
}