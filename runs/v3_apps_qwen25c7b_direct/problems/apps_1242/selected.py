def solve(s):
    n = len(s)
    result = [0] * n
    for i in range(1, n):
        if s[i] < s[i - 1]:
            result[i - 1] = 1
            s = s[:i][::-1] + s[i:]
    return result

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    result = solve(s)
    print(" ".join(map(str, result)))