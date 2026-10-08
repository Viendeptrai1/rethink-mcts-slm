import sys

def main():
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    C = int(data[2])

    # Check if there exists a non-negative integer k such that (k * A) % B == C
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