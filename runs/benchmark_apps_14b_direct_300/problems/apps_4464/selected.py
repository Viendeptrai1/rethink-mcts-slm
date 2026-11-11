import sys

def main():
    import sys
    A, B, C = map(int, sys.stdin.read().split())
    
    # Check if it's possible to find a non-negative integer k such that (k * A) % B == C
    if C % gcd(A, B) == 0:
        print("YES")
    else:
        print("NO")

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    main()