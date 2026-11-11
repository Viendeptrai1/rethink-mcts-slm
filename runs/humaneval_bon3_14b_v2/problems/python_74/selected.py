def total_match(lst1, lst2):
    total_chars_lst1 = sum(len(s) for s in lst1)
    total_chars_lst2 = sum(len(s) for s in lst2)
    
    if total_chars_lst1 < total_chars_lst2:
        return lst1
    else:
        return lst2

# Example usage:
# print(total_match([], []))  # ➞ []
# print(total_match(['hi', 'admin'], ['hI', 'Hi']))  # ➞ ['hI', 'Hi']
# print(total_match(['hi', 'admin'], ['hi', 'hi', 'admin', 'project']))  # ➞ ['hi', 'admin']
# print(total_match(['hi', 'admin'], ['hI', 'hi', 'hi']))  # ➞ ['hI', 'hi', 'hi']
# print(total_match(['4'], ['1', '2', '3', '4', '5']))  # ➞ ['4']