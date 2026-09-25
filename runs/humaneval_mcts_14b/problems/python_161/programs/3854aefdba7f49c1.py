def solve(s):
    if any(c.isalpha() for c in s):
        return ''.join(c.swapcase() if c.isalpha() else c for c in s)
    else:
        return s[::-1]

# Test cases
print(solve("1234"))  # Output: "4321"
print(solve("ab"))    # Output: "AB"
print(solve("#a@C"))  # Output: "#A@c"