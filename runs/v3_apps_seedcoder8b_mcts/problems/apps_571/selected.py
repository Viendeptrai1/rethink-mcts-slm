def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    # To store the result
    result = list(s)
    
    # Stack to track the positions of '('
    stack = []
    
    # First pass: replace '?' with '(' and track positions of '('
    for i in range(n):
        if s[i] == '(':
            stack.append(i)
        elif s[i] == '?':
            result[i] = '('
            stack.append(i)
    
    # Second pass: replace remaining '?' with ')'
    for i in range(n):
        if s[i] == '?':
            result[i] = ')'
    
    # Check if all strict prefixes are not correct parenthesis sequences
    def is_correct_parenthesis_sequence(seq):
        balance = 0
        for char in seq:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            if balance < 0:
                return False
        return balance == 0
    
    # Check all strict prefixes
    for i in range(1, n):
        if is_correct_parenthesis_sequence(result[:i]):
            print(":((")
            return
    
    # If all strict prefixes are not correct, print the result
    print("".join(result))