import sys

def count_factors_of_5(n):
    count = 0
    power_of_5 = 5
    while n >= power_of_5:
        count += n // power_of_5
        power_of_5 *= 5
    return count

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = count_factors_of_5(n)
    sys.stdout.write(str(result))