def find_original_message(t):
    n = len(t)
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            s = t[:i]
            if t == s * (n // i):
                return "NO"
    
    for i in range(1, n):
        s = t[:i]
        if t == s * (n // len(s)) + t[i:]:
            return f"YES\n{s}"
    
    return "NO"

t = input().strip()
print(find_original_message(t))