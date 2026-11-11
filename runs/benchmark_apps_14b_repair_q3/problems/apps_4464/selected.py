import sys

def main():
    import sys
    A, B, C = map(int, sys.stdin.read().split())
    
    # Check if it's possible to find a non-negative integer k such that (k * A) % B == C
    # This is equivalent to checking if there exists a k such that k * A ≡ C (mod B)
    # Since A and B are both positive, we can use the property of modular arithmetic:
    # If gcd(A, B) divides C, then there exists such a k.
    
    from math import gcd
    
    if C % gcd(A, B) == 0:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()