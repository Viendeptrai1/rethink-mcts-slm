import sys

def can_sort_with_ravioli(n, arr):
    def simulate_ravioli_sort(arr):
        while len(arr) > 1:
            max_height = max(arr)
            max_index = arr.index(max_height)
            
            # Check for sliding condition
            if max_index > 0 and arr[max_index] - arr[max_index - 1] >= 2:
                return False
            if max_index < len(arr) - 1 and arr[max_index] - arr[max_index + 1] >= 2:
                return False
            
            # Remove the tallest stack
            arr.pop(max_index)
        
        return True

    if simulate_ravioli_sort(arr[:]):
        return "YES"
    else:
        return "NO"

# Read input
n = int(sys.stdin.readline().strip())
arr = list(map(int, sys.stdin.readline().strip().split()))

# Output result
print(can_sort_with_ravioli(n, arr))