import sys

def find_lis_length(arr):
    n = len(arr)
    lis = [1] * n
    for i in range(1, n):
        for j in range(0, i):
            if arr[i] > arr[j] and lis[i] < lis[j] + 1:
                lis[i] = lis[j] + 1
    return max(lis)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = list(map(int, data[1:]))
    
    lis_length = find_lis_length(p)
    result = n - lis_length
    
    print(result)

if __name__ == "__main__":
    main()