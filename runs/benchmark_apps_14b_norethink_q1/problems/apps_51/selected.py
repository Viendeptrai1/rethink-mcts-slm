import sys

def find_overlap(s):
    n = len(s)
    for i in range(1, n // 2 + 1):
        if s.startswith(s[i:]):
            return s[:n - i]
    return None

def main():
    import sys
    t = sys.stdin.read().strip()
    
    s = find_overlap(t)
    if s:
        print("YES")
        print(s)
    else:
        print("NO")

if __name__ == "__main__":
    main()