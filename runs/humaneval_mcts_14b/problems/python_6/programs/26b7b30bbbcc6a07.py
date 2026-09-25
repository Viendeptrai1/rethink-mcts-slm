from typing import List

def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    """
    # Split the input string into individual groups based on spaces
    groups = paren_string.split()
    
    # Initialize a list to store the maximum depth for each group
    max_depths = []
    
    # Iterate through each group
    for group in groups:
        current_depth = 0
        max_depth = 0
        
        # Iterate through each character in the group
        for char in group:
            if char == '(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == ')':
                current_depth -= 1
        
        # Append the maximum depth for this group to the list
        max_depths.append(max_depth)
    
    return max_depths