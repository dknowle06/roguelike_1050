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
    def __init__(self, healing:float, damage:float, *args:float):
        self.healing = healing
        self.damage = damage

        self.stat_boosts = {}
        
        for arg in args:
            self.stat_boosts


ENEMY_ACTIONS_DICT = {}