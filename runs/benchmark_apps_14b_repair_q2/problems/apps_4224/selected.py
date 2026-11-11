import sys

def max_operations(N, a):
    total_ops = 0
    for num in a:
        ops = 0
        # Divide by 2 as many times as possible
        while num % 2 == 0:
            num //= 2
            ops += 1
        # Multiply by 3 as many times as possible
        while num % 3 == 0:
            num //= 3
            ops += 1
        # If num is reduced to 1, add the number of operations to total_ops
        if num == 1:
            total_ops += ops
    return total_ops

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    a = list(map(int, data[1:]))
    print(max_operations(N, a))