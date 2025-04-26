"""
4/24/2025
David Knowles 

File that stores common functions that are used by multiple files. 
There is very little cohesion in this file. 

Also stores the sets that contains valid commands 
"""

# sets that store valid player commands 
# `EVERYDAY_COMMS` shouldn't be used, it's only here to be unioned to create the attack and shop command sets 
EVERYDAY_COMMS = {"INVENTORY", "MAP", "SELF", "ITEM"}
ATTACK_COMMS = EVERYDAY_COMMS | {"CHECK", "ATTACK", "EQUIP", "USE"}
SHOP_COMMS = EVERYDAY_COMMS | {"BUY", "SELL"}
NAVIGATION_COMMS = EVERYDAY_COMMS | {"NEXT", "CONTINUE"} # next and continue will do the same thing 

VALID_ACTION = "Please choose a valid action!\n"

# prints `num` newlines
def newline(num:int = 1):
    for i in range(num):
        print() # prints a blank line 

# recursive function that validates user input 
# `test_case` should be a lambda or a function that returns a boolean value 
# `msg` is the string that is printed to prompt the user for input 
# `yell` is the string that is printed to yell at the user for bad input 
def input_validation(msg:str, yell:str, test_case):
    print(msg, end="")

    # takes user input, strips whitespace, and converts the input to uppercase
    user_input = input().strip().upper()

    if test_case(user_input):
        return user_input
    else:
        print(yell, end="")
        return input_validation(msg, yell, test_case)
    
# converts a list to a string, used during the gameloop
def list_to_string(arr:list) -> str:
    counter = 1
    output = ""

    for i in arr:
        output += f"[{counter}] {i}, "
        counter += 1

    return output[:-2]