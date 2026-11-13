import sys
import math

def find_squares(n):
    # We need to find integers m, k such that n = m^2 - k^2
    # m^2 - k^2 = n
    # m = k + sqrt(n) or m = k - sqrt(n)
    # Since m and k need to be integers, m = k + sqrt(n) is our primary interest.
    # If n < 0, then it's impossible since sqrt(n) won't be an integer.
    if n < 0:
        print("impossible")
        return
    
    # Start with possible m values and check corresponding k values
    for m in range(int(math.isqrt(n)) + 1, n + 1):
        k_squared = m * m - n
        if k_squared < 0:
            continue
        k = int(math.isqrt(k_squared))
        if k * k == k_squared:
            print(m, k)
            return
    
    print("impossible")

def main():
    input_data = sys.stdin.read().strip()
    n = int(input_data)
    find_squares(n)

if __name__ == "__main__":
    main()