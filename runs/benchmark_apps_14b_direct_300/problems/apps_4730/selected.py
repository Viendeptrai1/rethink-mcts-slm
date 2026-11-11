def validate_delimiters():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    L = int(data[0])
    program = data[1]
    
    stack = []
    matching_bracket = {')': '(', ']': '[', '}': '{'}
    
    for i, char in enumerate(program):
        if char in "([{":
            stack.append((char, i))
        elif char in ")]}":
            if not stack or stack[-1][0] != matching_bracket[char]:
                print(f"{char} {i}")
                return
            stack.pop()
    
    if not stack:
        print("ok so far")
    else:
        print("ok so far")

validate_delimiters()