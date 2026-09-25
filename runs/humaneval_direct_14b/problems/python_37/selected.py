def sort_even(l: list):
    """This function takes a list l and returns a list l' such that
    l' is identical to l in the odd indicies, while its values at the even indicies are equal
    to the values of the even indicies of l, but sorted.
    """
    # Extract elements at even indices
    even_elements = [l[i] for i in range(0, len(l), 2)]
    # Sort the even elements
    even_elements.sort()
    
    # Create a new list to store the result
    result = l[:]
    
    # Replace elements at even indices with sorted ones
    even_index = 0
    for i in range(0, len(l), 2):
        result[i] = even_elements[even_index]
        even_index += 1
    
    return result

# Test cases
print(sort_even([1, 2, 3]))  # Output: [1, 2, 3]
print(sort_even([5, 6, 3, 4]))  # Output: [3, 6, 5, 4]