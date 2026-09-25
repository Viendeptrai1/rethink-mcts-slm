import sys

def can_sort_with_ravioli(n, arr):
    def simulate_sort(arr):
        while len(arr) > 0:
            max_height = max(arr)
            max_index = arr.index(max_height)
            
            # Check for sliding condition
            for i in range(len(arr) - 1):
                if abs(arr[i] - arr[i + 1]) >= 2:
                    return False
            
            # Remove the tallest stack
            arr.pop(max_index)
        
        return True

    if simulate_sort(arr[:]):
        print("YES")
    else:
        print("NO")

# Read input
n = int(sys.stdin.readline().strip())
arr = list(map(int, sys.stdin.readline().strip().split()))

# Output result
can_sort_with_ravioli(n, arr)