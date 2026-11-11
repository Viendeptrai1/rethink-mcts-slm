import sys

def thanos_sort_max_length(n, arr):
    def is_sorted(subarr):
        return all(subarr[i] <= subarr[i + 1] for i in range(len(subarr) - 1))
    
    def max_sorted_length(arr, start, end):
        if start >= end:
            return 0
        if is_sorted(arr[start:end]):
            return end - start
        
        mid = (start + end) // 2
        left_length = max_sorted_length(arr, start, mid)
        right_length = max_sorted_length(arr, mid, end)
        
        return max(left_length, right_length)
    
    return max_sorted_length(arr, 0, n)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))
    result = thanos_sort_max_length(n, arr)
    print(result)