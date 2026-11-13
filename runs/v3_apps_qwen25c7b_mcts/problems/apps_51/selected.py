def check_error(t):
    n = len(t)
    for i in range(1, n // 2 + 1):
        if t[:i] == t[i:i+i]:
            return "YES", t[:i]
    return "NO", ""

# Example usage:
t = input().strip()
result, s = check_error(t)
print(result)
if result == "YES":
    print(s)