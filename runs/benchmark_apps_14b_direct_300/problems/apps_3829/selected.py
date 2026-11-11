import sys
import math

def expected_max(m, n):
    # Calculate the expected maximum value
    total_sum = 0.0
    for i in range(1, m + 1):
        total_sum += i * (1 - ((i - 1) / m) ** n)
    
    return total_sum

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    m = int(data[0])
    n = int(data[1])
    result = expected_max(m, n)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()