def sorted_list_sum(lst):
    # Filter out strings with odd lengths
    filtered_lst = [s for s in lst if len(s) % 2 == 0]
    
    # Sort the list by length, then alphabetically
    sorted_lst = sorted(filtered_lst, key=lambda x: (len(x), x))
    
    return sorted_lst