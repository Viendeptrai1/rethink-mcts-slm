import sys

def solve(s):
    n = len(s)
    result = [0] * n
    s = list(s)
    
    for i in range(n):
        if s[i] == 'b':
            # Find the next 'a' to swap with
            j = i + 1
            while j < n and s[j] == 'b':
                j += 1
            if j < n:
                # Swap s[i] with s[j]
                s[i], s[j] = s[j], s[i]
                result[i] = 1
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    result = solve(data)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()