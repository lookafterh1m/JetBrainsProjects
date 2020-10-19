# finish the function
def find_the_parent(child):
    shelves = (Drinks, Pastry, Sweets)
    for shelve in shelves:
        if issubclass(child, shelve):
            print(shelve.__name__)
            break
