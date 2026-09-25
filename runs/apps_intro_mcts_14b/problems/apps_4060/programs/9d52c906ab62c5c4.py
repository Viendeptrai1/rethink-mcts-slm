import sys

def count_positions_to_make_regular(n, s):
    # Initialize variables
    balance = 0
    max_balance = 0
    result = 0
    
    # First pass: calculate the maximum balance
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        max_balance = max(max_balance, balance)
    
    # Reset balance for the second pass
    balance = 0
    
    # Second pass: count positions where changing the bracket makes the sequence regular
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        
        # Check if changing this bracket makes the sequence regular
        if (char == '(' and balance - 2 + max_balance >= 0) or (char == ')' and balance + 2 + max_balance >= 0):
            result += 1
    
    return result

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Calculate and print the result
print(count_positions_to_make_regular(n, s))