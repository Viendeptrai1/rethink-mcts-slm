import sys

def count_trailing_zeros(n):
    count = 0
    power_of_5 = 5
    while n >= power_of_5:
        count += n // power_of_5
        power_of_5 *= 5
    return count

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    print(count_trailing_zeros(n))