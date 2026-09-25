def match_parens(lst):
    # Extract the two strings from the list
    s1, s2 = lst
    
    # Function to calculate the net balance of parentheses in a string
    def net_balance(s):
        balance = 0
        min_balance = 0
        for char in s:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            min_balance = min(min_balance, balance)
        return balance, min_balance
    
    # Calculate net balance and minimum balance for both strings
    balance1, min_balance1 = net_balance(s1)
    balance2, min_balance2 = net_balance(s2)
    
    # Check if concatenating s1 + s2 results in a balanced string
    if balance1 + min_balance2 >= 0 and balance2 + min_balance1 >= 0:
        return 'Yes'
    
    # Check if concatenating s2 + s1 results in a balanced string
    if balance2 + min_balance1 >= 0 and balance1 + min_balance2 >= 0:
        return 'Yes'
    
    return 'No'

# Example usage
print(match_parens(['()(', ')']))  # Output: 'Yes'
print(match_parens([')', ')']))    # Output: 'No'