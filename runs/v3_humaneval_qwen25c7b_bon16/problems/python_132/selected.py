def is_nested(s):
    stack = []
    has_nested = False

    for char in s:
        if char == '[':
            stack.append(char)
        elif char == ']' and stack:
            stack.pop()
            if stack:
                has_nested = True

    return has_nested and not stack