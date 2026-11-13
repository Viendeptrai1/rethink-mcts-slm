def validate_delimiters():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    L = int(data[0].strip())
    program = data[1].strip()
    
    stack = []
    matching_delimiter = {')': '(', ']': '[', '}': '{'}
    
    for i, char in enumerate(program):
        if char in '([{':
            stack.append((char, i))
        elif char in ')]}':
            if not stack or stack[-1][0] != matching_delimiter[char]:
                print(f"{char} {i}")
                return
            stack.pop()
    
    if stack:
        print("ok so far")
    else:
        print("ok so far")