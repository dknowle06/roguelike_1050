"""
David Knowles
4/7/2025

Contains functions that return `Enemy_Action` objects
These objects contain information about stat boosts, healing, damage, etc. 

"""

# consts that store damage types
PHYSICAL = 1
SPECIAL  = 2
PIERCING = 3

"""
Physical damage is damage dealt with regular weapons

Special damage is damage dealt with magic 

Piercing damage is damage that ignores player and enemy stats (Might remain unused in the final build?)
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
    def __init__(self, healing:float, damage:float, enemy_name:str, attack_verb:str, damage_type:int = PHYSICAL, **kwargs):
        self.healing = healing
        self.damage = damage

        self.enemy_name = enemy_name
        self.attack_verb = attack_verb

        self.stat_boosts = {}

        self.damage_type = damage_type
        
        for key, value in kwargs.items():
            # using the type casts i define in `Stat_Boost` here instead of normal getters or setters
            # probably not as clear in the code for what it does but it's a little more concise i think 
            self.stat_boosts[key] = value

    # string :-)
    def __str__(self) -> str:
        output_str = f"{self.enemy_name} {self.attack_verb}!\n"

        if self.damage != 0:
            output_str += f"{self.enemy_name} hit you for {self.damage} {get_damage_type(self.damage_type)} damage." if self.damage > 0 else f"{self.enemy_name} healed you for {-1 * self.damage} hp."
            output_str += "\n"

        if self.healing != 0:
            output_str += f"{self.enemy_name} healed itself for {self.healing} hp." if self.healing > 0 else f"{self.enemy_name} dealt {-1 * self.healing} damage to itself."
            output_str += "\n"

        return output_str[:-1]

    # modifies the damage amount based on enemy and player stats
    def mod_damage(self, enemy_stats:dict, player_stats:dict) -> None:

        # realistically i should be using try/catch here to be safe
        # but if these aren't defined in the dictionaries passed, there is a major issue happening somewhere else
        # essentially, not this function's problem!!!
        player_defense = player_stats["Defense"]
        enemy_attack = enemy_stats["Attack"]

        player_sp_defense = player_stats["Special Defense"]
        enemy_sp_attack = enemy_stats["Special Attack"]

        # ends the function execution if the enemy is actually healing the player, or if the enemy deals no damage
        if self.damage <= 0:
            return None

        # increase damage based on enemy damage stat, and then decrease it based on player defensive stat

        # don't modify piercing damage!! 

        if self.damage_type == PHYSICAL:
            self.damage = self.damage * (enemy_attack + 100) / 100
            self.damage = self.damage / ((player_defense + 100) / 100)

        elif self.damage_type = SPECIAL:
            self.damage = self.damage * (enemy_sp_attack + 100) / 100
            self.damage = self.damage / ((player_sp_defense + 100) / 100)



# FUNCTION SECTION
# all functions should be defined as:
"""
def foo(stats_dict:dict, enemy_name:str):
    \*math stuff here\*
    return `Enemy_Action`
"""

# healing, damage, enemy name, attack verb, status effects (TODO), stat buffs


def flop(stats_dict:dict, enemy_name:str):
    return Enemy_Action(0, 1, enemy_name, "flopped around", PHYSICAL)

def cough(stats_dict:dict, enemy_name:str):
    return Enemy_Action(-1, 0, enemy_name, "coughed", PHYSICAL)

# FUNCTION DICTIONARY
ENEMY_ACTIONS_DICT = {
    "flop":flop,
    "cough":cough
}