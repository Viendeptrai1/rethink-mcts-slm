def match_parens(lst):
    # Count the total number of open and close parentheses
    open_count = sum(s.count('(') for s in lst)
    close_count = sum(s.count(')') for s in lst)
    
    # If the number of open and close parentheses are equal, it might be possible to balance them
    if open_count == close_count:
        return 'Yes'
    else:
        return 'No'