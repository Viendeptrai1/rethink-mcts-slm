import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(input_data[i+1]) for i in range(n)]
    
    def get_max_sorted_length(arr):
        if len(arr) <= 1:
            return len(arr)
        
        # Check if the current array is sorted
        is_sorted = all(arr[i] <= arr[i+1] for i in range(len(arr)-1))
        if is_sorted:
            return len(arr)
        
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        return max(get_max_sorted_length(left_half), get_max_sorted_length(right_half))
    
    print(get_max_sorted_length(a))

if __name__ == "__main__":
    solve()