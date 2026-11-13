def solve(s):
    n = len(s)
    for i in range(n, 0, -1):
        for j in range(n - i + 1):
            t = s[j:j+i]
            if t == t[::-1] and s.startswith(t[:len(s)//2]) and s.endswith(t[len(s)//2:]):
                return t
    return s[0]

def main():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        print(solve(s))

if __name__ == "__main__":
    main()