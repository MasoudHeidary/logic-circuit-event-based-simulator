def all_same(lst):
    # Check if all elements in the list are equal to the first element
    return all(elem == lst[0] for elem in lst)