def solve(s):
    n = len(s)
    balance = 0
    result = []
    
    for char in s:
        if char == '(':
            balance += 1
            result.append('(')
        elif char == ')':
            balance -= 1
            result.append(')')
        else:  # char == '?'
            if balance < 0:
                balance += 1
                result.append('(')
            else:
                balance -= 1
                result.append(')')
        
        # Check if the current prefix is a valid parenthesis sequence
        if balance < 0:
            return ":("
    
    # Final check to ensure the entire sequence is valid
    if balance != 0:
        return ":("
    
    return ''.join(result)

# Read input
n = int(input().strip())
s = input().strip()

# Solve and print the result
print(solve(s))