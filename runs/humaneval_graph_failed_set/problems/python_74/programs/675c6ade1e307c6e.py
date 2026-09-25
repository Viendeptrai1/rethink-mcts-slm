def total_match(lst1, lst2):
    # Helper function to calculate total number of characters in a list
    def total_characters(lst):
        return sum(len(s) for s in lst)
    
    # Calculate the total number of characters in each list
    total_chars_lst1 = total_characters(lst1)
    total_chars_lst2 = total_characters(lst2)
    
    # Compare the total number of characters and return the appropriate list
    if total_chars_lst1 < total_chars_lst2:
        return lst1
    else:
        return lst2

# Test cases
print(total_match([], []))  # ➞ []
print(total_match(['hi', 'admin'], ['hI', 'Hi']))  # ➞ ['hI', 'Hi']
print(total_match(['hi', 'admin'], ['hi', 'hi', 'admin', 'project']))  # ➞ ['hi', 'admin']
print(total_match(['hi', 'admin'], ['hI', 'hi', 'hi']))  # ➞ ['hI', 'hi', 'hi']
print(total_match(['4'], ['1', '2', '3', '4', '5']))  # ➞ ['4']