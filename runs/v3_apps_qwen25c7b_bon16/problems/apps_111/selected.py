import sys

def find_kth_smallest_divisor(n, k):
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    divisors.sort()
    return divisors[k - 1] if k <= len(divisors) else -1

input_line = sys.stdin.readline().strip()
n, k = map(int, input_line.split())

result = find_kth_smallest_divisor(n, k)
print(result)