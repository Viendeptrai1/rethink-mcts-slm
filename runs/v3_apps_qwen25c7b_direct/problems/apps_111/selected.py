import sys

def find_kth_divisor(n, k):
    count = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            count += 1
            if count == k:
                return i
            if i != n // i:
                count += 1
                if count == k:
                    return n // i
    return -1

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    result = find_kth_divisor(n, k)
    print(result)