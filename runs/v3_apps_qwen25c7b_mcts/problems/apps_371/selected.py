import math

def min_n(m):
    if m == 1:
        return 8
    elif m % 2 != 0:
        return -1
    else:
        k = 2
        while True:
            total_ways = 0
            current_ways = 1
            while current_ways <= m:
                total_ways += current_ways
                current_ways *= k
            if total_ways == m:
                return (k**4 - 1) // (k - 1)
            elif total_ways > m:
                break
            k += 1
    return -1

# Example usage:
m = int(input().strip())
print(min_n(m))