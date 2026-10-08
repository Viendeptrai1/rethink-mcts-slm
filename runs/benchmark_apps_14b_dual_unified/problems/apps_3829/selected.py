import sys
import math

def expected_maximum(m, n):
    # Calculate the expected maximum value using the formula
    return sum(i * ((i ** n - (i - 1) ** n) / m ** n) for i in range(1, m + 1))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    m = int(data[0])
    n = int(data[1])
    result = expected_maximum(m, n)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()