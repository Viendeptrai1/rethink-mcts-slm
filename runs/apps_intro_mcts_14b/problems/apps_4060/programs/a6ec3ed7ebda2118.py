import sys

def count_positions_to_make_regular(n, s):
    # Calculate the balance of the original sequence
    balance = 0
    min_balance = 0
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        min_balance = min(min_balance, balance)
    
    # If the original sequence is already regular, no changes are needed
    if balance == 0 and min_balance >= 0:
        return 0
    
    # Count the number of positions where changing a bracket makes the sequence regular
    count = 0
    current_balance = 0
    for i in range(n):
        if s[i] == '(':
            current_balance += 1
        else:
            current_balance -= 1
        
        # Check if changing this bracket makes the sequence regular
        if (s[i] == '(' and current_balance - 1 == 0 and current_balance - 1 >= min_balance) or \
           (s[i] == ')' and current_balance + 1 == 0 and current_balance + 1 >= min_balance):
            count += 1
    
    return count

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Output the result
print(count_positions_to_make_regular(n, s))