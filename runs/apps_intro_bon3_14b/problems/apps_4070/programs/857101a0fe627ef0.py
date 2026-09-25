import sys

def count_factors(n):
    count = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            if i * i == n:
                count += 1
            else:
                count += 2
    return count

def main():
    n = int(sys.stdin.read().strip())
    result = count_factors(n)
    print(result)

if __name__ == "__main__":
    main()