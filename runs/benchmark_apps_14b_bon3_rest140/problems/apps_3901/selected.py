import sys
from math import gcd

def min_operations_to_one(n, arr):
    if 1 in arr:
        return n - arr.count(1)
    
    total_gcd = arr[0]
    for num in arr:
        total_gcd = gcd(total_gcd, num)
    
    if total_gcd != 1:
        return -1
    
    operations = 0
    for i in range(n):
        if arr[i] == 1:
            continue
        for j in range(i + 1, n):
            if arr[j] == 1:
                continue
            arr[i] = gcd(arr[i], arr[j])
            operations += 1
            if arr[i] == 1:
                break
    
    return operations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    arr = list(map(int, data[1:]))
    
    result = min_operations_to_one(n, arr)
    print(result)

if __name__ == "__main__":
    main()