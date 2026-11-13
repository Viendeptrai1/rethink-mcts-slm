import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = list(map(int, input_data[1:1+n]))
    
    # Check if an array is sorted (non-decreasing)
    def is_sorted(arr):
        for i in range(1, len(arr)):
            if arr[i] < arr[i-1]:
                return False
        return True
    
    # Recursive function to find the longest sorted subarray via Thanos sort
    def thanos_sort(arr):
        if len(arr) <= 1:
            return len(arr)
        
        if is_sorted(arr):
            return len(arr)
        
        half = len(arr) // 2
        left_half = arr[:half]
        right_half = arr[half:]
        
        return max(thanos_sort(left_half), thanos_sort(right_half))
    
    result = thanos_sort(a)
    print(result)

if __name__ == "__main__":
    solve()