import sys

def count_positions_to_make_regular(n, s):
    # Initialize variables
    balance = 0
    min_balance = 0
    count = 0
    
    # First pass: Calculate the minimum balance
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        min_balance = min(min_balance, balance)
    
    # Reset balance for the second pass
    balance = 0
    
    # Second pass: Count positions where changing the bracket makes the sequence regular
    for i, char in enumerate(s):
        if char == '(':
            balance += 1
        else:
            balance -= 1
        
        # Check if changing this bracket makes the sequence regular
        if (char == '(' and balance - 1 >= min_balance) or (char == ')' and balance + 1 >= min_balance):
            count += 1
    
    return count

# Read input
input = sys.stdin.read().split()
n = int(input[0])
s = input[1]

# Calculate and print the result
result = count_positions_to_make_regular(n, s)
print(result)