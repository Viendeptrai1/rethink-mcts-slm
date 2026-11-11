import sys
import math

def expected_max(m, n):
    # Calculate the expected value of the maximum of n dice rolls with m faces
    total_probability = 0.0
    for k in range(1, m + 1):
        probability = 1.0
        for i in range(n):
            probability *= (k / m)
        total_probability += k * probability
    
    return total_probability

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