import sys

def main():
    import sys
    m, n, t = map(int, sys.stdin.readline().split())
    
    if t == 1:
        result = n <= m
    elif t == 2:
        result = (1 << n) <= m
    elif t == 3:
        result = n**4 <= m
    elif t == 4:
        result = n**3 <= m
    elif t == 5:
        result = n**2 <= m
    elif t == 6:
        result = n * (n.bit_length() - 1) <= m
    elif t == 7:
        result = n <= m
    
    print("AC" if result else "TLE")

if __name__ == "__main__":
    main()