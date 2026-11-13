import sys

def find_divisor():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    arr = list(map(int, data[1:]))
    
    min_val = min(arr)
    
    for i in range(1, min_val + 1):
        if all(x % i == 0 for x in arr):
            return i
    
    return -1

if __name__ == "__main__":
    result = find_divisor()
    print(result)