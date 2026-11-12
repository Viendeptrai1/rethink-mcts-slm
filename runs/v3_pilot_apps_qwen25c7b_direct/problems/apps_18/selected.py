def min_lexicographical_string(s):
    stack = []
    result = []
    
    for char in s:
        while stack and stack[-1] < char:
            result.append(stack.pop())
        stack.append(char)
    
    while stack:
        result.append(stack.pop())
    
    return ''.join(result[::-1])

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    print(min_lexicographical_string(s))