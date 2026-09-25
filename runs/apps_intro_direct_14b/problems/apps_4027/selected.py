import sys

def min_difference(n):
    total_sum = n * (n + 1) // 2
    if total_sum % 2 == 0:
        return 0
    else:
        return 1

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = min_difference(n)
    sys.stdout.write(str(result))