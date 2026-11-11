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
        # If there are unmatched opening delimiters, we need to find the first one
        for char, index in stack:
            print(f"{matching_bracket[char]} {index}")
            return

# Call the function to execute the solution
validate_delimiters()