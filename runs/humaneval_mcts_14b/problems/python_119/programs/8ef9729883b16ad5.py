def match_parens(lst):
    # Count the number of open and close parentheses in each string
    open_count_1 = lst[0].count('(')
    close_count_1 = lst[0].count(')')
    open_count_2 = lst[1].count('(')
    close_count_2 = lst[1].count(')')

    # Check if concatenating in one order results in a balanced string
    if open_count_1 + open_count_2 == close_count_1 + close_count_2:
        # Check if there exists an order where the parentheses are balanced
        if (open_count_1 >= close_count_2) or (open_count_2 >= close_count_1):
            return 'Yes'
    
    return 'No'

# Test cases
print(match_parens(['()(', ')']))  # Output: 'Yes'
print(match_parens([')', ')']))    # Output: 'No'