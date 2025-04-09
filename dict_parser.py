"""
David Knowles
4/9/2025

Contains functions that parse a text file into a dictionary
First element will always be a string
Second elements will try and parse into a float, int, or string
essentially, only elementary types can be used 
"""

# returns a list of dictionaries
# this function is probably not very fast but like. it works. and i wrote it in like 10 minutes
# syntax is also gross. whatever. it works. idgaf.
def dict_parser(file_name:str, split_char:str = ":", clean_key:bool = False) -> list:
    output_dicts = []

    parsed_file = []

    try:

        with open(file_name, "r") as f:
            for line in f:
                # adds the parsed line and removes the last character if it is a linebreak
                # there is probably a smarter and cleaner and nicer looking way to do this than a ternary operator but idgaf
                parsed_file.append(line[:-1] if "\n" in line else line)

    # if the file doesn't exist, print an error message and exit the program 
    except FileNotFoundError as e:
        error_message = f"{e}\nEnsure that {file_name} has been downloaded from https://github.com/dknowle06/roguelike_1050 and is in the correct location.\nIf this file path exists and you still come across this issue, contact me at dknowle@clemson.edu."
        print(error_message)

        # create a crashlog
        c = open("crashlog.txt", "w")
        c.write(error_message)
        c.close()

        quit()

    temp_lines = []

    for line in parsed_file:
        if line == "{":
            # flush list
            temp_lines = []

        elif line == "}":
            # this is where converting into a dictionary happens

            temp_dict = {}

            # who needs descriptive variable name?
            for i in temp_lines:
                j = i.split(split_char)

                # try/except block allows me to cast to int or float without EXPLODING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! GULPAROONIES
                try:
                    if "." in j[1]:
                        j[1] = float(j[1])
                    else:
                        j[1] = int(j[1])
                except:
                    # removes surronding quotes if there are any 
                    # is there a smarter way to do this?
                    # yes
                    # do i care?
                    # no

                    if j[1][0] == "\"" and j[1][-1] == "\"":
                        j[1] = j[1][1:-1]

                    # adds linebreaks in
                    j[1] = j[1].replace("\\n","\n")

                # if `clean_key` is true, replace underscores with spaces and capitalize it 
                # `.title()` capitalizes the first letter of each word
                if clean_key:
                    j[0] = j[0].replace("_", " ").title()

                temp_dict[j[0]] = j[1]

            # casts to dict here because uhhhhh idk but i dont wanna change it 
            output_dicts.append(dict(temp_dict))

        elif line.strip() == "":
            # tells the program to skip any blank lines
            pass

        else:
            # add line to temporary array to be parsed into a dictionary
            temp_lines.append(line.strip())



    return output_dicts