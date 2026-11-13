def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    # Function to check if a sequence is a correct parenthesis sequence
    def is_correct(seq):
        balance = 0
        for char in seq:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            if balance < 0:
                return False
        return balance == 0
    
    # Try to replace '?' with '(' or ')'
    result = list(s)
    for i in range(n):
        if result[i] == '?':
            # Try replacing '?' with '('
            result[i] = '('
            if is_correct(result[:i+1]):
                result[i] = ')'
            else:
                result[i] = '('
    
    # Check if the final sequence is a correct parenthesis sequence
    if is_correct(result):
        print("".join(result))
    else:
        print(":( ")