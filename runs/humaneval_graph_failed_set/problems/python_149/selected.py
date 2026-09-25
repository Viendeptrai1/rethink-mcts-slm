def sorted_list_sum(lst):
    # Filter out strings with odd lengths
    even_length_strings = [s for s in lst if len(s) % 2 == 0]
    
    # Sort the list first by length, then alphabetically
    sorted_strings = sorted(even_length_strings, key=lambda s: (len(s), s))
    
    return sorted_strings