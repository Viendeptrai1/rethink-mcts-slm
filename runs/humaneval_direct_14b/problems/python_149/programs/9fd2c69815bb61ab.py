def sorted_list_sum(lst):
    # Filter out strings with odd lengths
    filtered_lst = [s for s in lst if len(s) % 2 == 0]
    
    # Sort the list first alphabetically, then by length
    sorted_lst = sorted(filtered_lst)
    
    return sorted_lst

# Example usage:
# assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]
# assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]