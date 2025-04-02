import mapgeneration

# executes code only inside of this `if` statement
if __name__ == "__main__":
    mapgeneration.set_seed(5)

    my_map = mapgeneration.create_map()

    print(my_map)