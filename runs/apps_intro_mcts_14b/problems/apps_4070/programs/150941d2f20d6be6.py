import sys

def count_factors_of_5(n):
    count = 0
    power_of_5 = 5
    while power_of_5 <= n:
        count += n // power_of_5
        power_of_5 *= 5
    return count

def main():
    import sys
    n = int(sys.stdin.read().strip())
    print(count_factors_of_5(n))

if __name__ == "__main__":
    main()