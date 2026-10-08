import sys
from math import log, ceil

def find_smallest_n(m):
    if m == 1:
        return 8
    
    for n in range(1, 10**15 + 1):
        count = 0
        for k in range(2, n):
            max_power = int(log(n, k))
            if max_power < 3:
                continue
            for i in range(max_power + 1):
                for j in range(i + 1, max_power + 1):
                    for l in range(j + 1, max_power + 1):
                        if k**i + k**j + k**l + k**max_power <= n:
                            count += 1
        if count == m:
            return n
    return -1

def main():
    import sys
    m = int(sys.stdin.read().strip())
    result = find_smallest_n(m)
    print(result)

if __name__ == "__main__":
    main()