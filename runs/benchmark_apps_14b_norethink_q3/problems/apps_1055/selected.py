import sys

def thanos_sort_max_length(n, arr):
    def is_sorted(subarr):
        return all(subarr[i] <= subarr[i + 1] for i in range(len(subarr) - 1))
    
    max_length = 0
    
    # Check all possible subarrays that are powers of 2 in size
    for size in [2**i for i in range(n.bit_length())]:
        for start in range(0, n, size):
            end = start + size
            if end <= n and is_sorted(arr[start:end]):
                max_length = max(max_length, size)
    
    return max_length

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    arr = list(map(int, data[1:]))
    
    print(thanos_sort_max_length(n, arr))

if __name__ == "__main__":
    main()