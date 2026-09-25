def sorted_list_sum(lst):
    # Step 1: Filter out strings with odd lengths
    filtered_lst = [s for s in lst if len(s) % 2 == 0]
    
    # Step 2: Sort the list by length, then alphabetically
    sorted_lst = sorted(filtered_lst, key=lambda x: (len(x), x))
    
    return sorted_lst

# Example usage:
# assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]
# assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]