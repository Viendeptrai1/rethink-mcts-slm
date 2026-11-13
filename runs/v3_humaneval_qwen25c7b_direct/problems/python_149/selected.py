def sorted_list_sum(lst):
    # Filter out strings with odd lengths
    even_length_lst = [word for word in lst if len(word) % 2 == 0]
    
    # Sort the list by length, then alphabetically
    sorted_lst = sorted(even_length_lst, key=lambda x: (len(x), x))
    
    return sorted_lst