def max_accordion_length(s):
    open_bracket = '['
    close_bracket = ']'
    colon = ':'
    vertical_line = '|'

    stack = []
    max_length = 0

    for char in s:
        if char == open_bracket:
            stack.append(char)
        elif char == close_bracket:
            if stack and stack[-1] == open_bracket:
                stack.pop()
                if stack and stack[-1] == colon:
                    start_index = len(stack) - 1
                    count_colons = 0
                    count_lines = 0
                    while stack and stack[-1] == colon:
                        stack.pop()
                        count_colons += 1
                    while stack and stack[-1] == vertical_line:
                        stack.pop()
                        count_lines += 1
                    stack.append(open_bracket)
                    stack.extend([colon] * count_colons)
                    stack.extend([vertical_line] * count_lines)
                    stack.append(close_bracket)
                    max_length = max(max_length, 2 + 2 * count_colons + count_lines)
        elif char == colon and stack and stack[-1] == open_bracket:
            stack.append(char)
        elif char == vertical_line and stack and stack[-1] in [open_bracket, colon]:
            stack.append(char)

    return max_length if max_length > 0 else -1

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(max_accordion_length(input))