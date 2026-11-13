def validate_delimiters(length, program):
    # Stack to keep track of opening delimiters
    stack = []
    # Dictionary to map closing delimiters to their corresponding opening delimiters
    matching_delimiter = {')': '(', ']': '[', '}': '{'}
    
    for i, char in enumerate(program):
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != matching_delimiter[char]:
                return f"{char} {i}"
            stack.pop()
    
    if stack:
        return 'ok so far'
    else:
        return 'ok so far'

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    length = int(data[0])
    program = data[1]
    
    result = validate_delimiters(length, program)
    print(result)