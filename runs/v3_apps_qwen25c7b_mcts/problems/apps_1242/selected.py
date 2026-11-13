def solve(s):
    n = len(s)
    result = [0] * n
    for i in range(n):
        prefix = s[:i+1]
        reversed_prefix = prefix[::-1]
        suffix = s[i+1:]
        if reversed_prefix < prefix and reversed_prefix <= suffix:
            result[i] = 1
    return result

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    result = solve(s)
    print(" ".join(map(str, result)))