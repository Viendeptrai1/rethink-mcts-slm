import sys
import math

def find_exponent(a):
    if a == 1:
        return 0
    if (a & (a - 1)) == 0:
        return int(math.log2(a))
    else:
        return int(math.log2(a) + 1)

if __name__ == "__main__":
    a = int(sys.stdin.read().strip())
    result = find_exponent(a)
    print(result)