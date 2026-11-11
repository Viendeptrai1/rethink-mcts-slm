import sys

def main():
    import sys
    A, B, C = map(int, sys.stdin.read().split())
    
    # Check if there exists a multiple of A such that (k * A) % B == C
    for k in range(1, B + 1):
        if (k * A) % B == C:
            print("YES")
            return
    
    print("NO")

if __name__ == "__main__":
    main()